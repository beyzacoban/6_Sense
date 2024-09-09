import random
import time
from flask import Flask, render_template_string, jsonify
from threading import Thread
import osmnx as ox
import networkx as nx
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Global variables
current_location = None
target_location = None
route = None
graph = None
obstacles = []
total_distance = 0
total_obstacles_avoided = 0
average_accessibility_score = 1.0
route_changes = 0

# Istanbul coordinates
ISTANBUL_CENTER = (41.0082, 28.9784)

def initialize_graph():
    global graph, current_location, target_location
    current_location = (41.0082, 28.9784)  # Istanbul, Sultanahmet Square
    target_location = (41.0136, 28.9833)   # Istanbul, Topkapi Palace
    print(f"Start location: {current_location}")
    print(f"Target location: {target_location}")

    graph = ox.graph_from_point(current_location, dist=2000, network_type='walk', custom_filter='["highway"~"footway|path|pedestrian|steps|crossing"]')
    
    for node, data in graph.nodes(data=True):
        accessibility = get_node_accessibility(data)
        for _, _, edge_data in graph.edges(node, data=True):
            edge_data['accessibility'] = accessibility

    print("Graph created with accessibility weights.")

def get_route(start, end):
    start_node = ox.nearest_nodes(graph, start[1], start[0])
    end_node = ox.nearest_nodes(graph, end[1], end[0])
    route = nx.shortest_path(graph, start_node, end_node, weight='accessibility')
    return [[graph.nodes[node]['y'], graph.nodes[node]['x']] for node in route]

def detect_obstacles(current_loc):
    if random.random() < 0.1:
        lat = current_loc[0] + random.uniform(-0.0001, 0.0001)
        lon = current_loc[1] + random.uniform(-0.0001, 0.0001)
        new_obstacle = (lat, lon)
        if new_obstacle not in obstacles:
            obstacles.append(new_obstacle)
            return True
    return False

def create_alternative_route(start, end, obstacles):
    temp_graph = graph.copy()
    for obstacle in obstacles:
        nearest_node = ox.nearest_nodes(temp_graph, obstacle[1], obstacle[0])
        if nearest_node in temp_graph:
            temp_graph.remove_node(nearest_node)
    try:
        route = nx.shortest_path(temp_graph, 
                                 ox.nearest_nodes(temp_graph, start[1], start[0]),
                                 ox.nearest_nodes(temp_graph, end[1], end[0]),
                                 weight='accessibility')
        return [[temp_graph.nodes[node]['y'], temp_graph.nodes[node]['x']] for node in route]
    except nx.NetworkXNoPath:
        print("No path found. Keeping original route.")
        return get_route(start, end)

def get_node_accessibility(tags):
    accessibility = 1.0
    if tags.get('tactile_paving') == 'yes': accessibility *= 0.8
    if tags.get('sidewalk') in ['left', 'right', 'both']: accessibility *= 0.7
    if tags.get('highway') == 'crossing' and tags.get('crossing') == 'traffic_signals': accessibility *= 0.6
    if tags.get('kerb') == 'lowered' or tags.get('curb_ramp') == 'yes': accessibility *= 0.8
    if tags.get('surface') in ['asphalt', 'concrete']: accessibility *= 0.9
    if tags.get('lit') == 'yes': accessibility *= 0.9
    return accessibility

@app.route('/')
def index():
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Blind Pedestrian Navigation - Istanbul</title>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
        <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 20px; }
            #map { height: 600px; width: 100%; }
            #info-panel { 
                margin-top: 20px; 
                display: flex; 
                justify-content: space-between;
            }
            #status, #accessibility { 
                flex: 1; 
                margin-right: 20px; 
                background-color: #f0f0f0; 
                padding: 10px; 
                border-radius: 5px;
            }
            #metrics { 
                display: flex; 
                flex-wrap: wrap;
                justify-content: space-around; 
                background-color: #e9ecef; 
                padding: 10px; 
                border-radius: 5px;
            }
            .metric { 
                text-align: center; 
                padding: 10px; 
                background-color: white; 
                border-radius: 5px; 
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                margin: 5px;
                min-width: 120px;
            }
            .metric-value { 
                font-size: 24px; 
                font-weight: bold; 
                color: #007bff;
            }
            .metric-label { 
                font-size: 14px; 
                color: #6c757d;
            }
            .legend {
                line-height: 18px;
                color: #555;
                background-color: white;
                padding: 6px 8px;
                border-radius: 5px;
            }
            .legend i {
                width: 18px;
                height: 18px;
                float: left;
                margin-right: 8px;
                opacity: 0.7;
            }
        </style>
    </head>
    <body>
        <h1>Blind Pedestrian Navigation Simulation</h1>
        <div id="map"></div>
        <div id="info-panel">
            <div id="status"></div>
            <div id="accessibility"></div>
        </div>
        <div id="metrics">
            <div class="metric">
                <div class="metric-value" id="total-distance">0</div>
                <div class="metric-label">Total Distance (km)</div>
            </div>
            <div class="metric">
                <div class="metric-value" id="obstacles-avoided">0</div>
                <div class="metric-label">Obstacles Avoided</div>
            </div>
            <div class="metric">
                <div class="metric-value" id="accessibility-score">1.00</div>
                <div class="metric-label">Avg. Accessibility Score</div>
            </div>
            <div class="metric">
                <div class="metric-value" id="route-changes">0</div>
                <div class="metric-label">Route Changes</div>
            </div>
        </div>
        <script>
            var map = L.map('map').setView([41.0082, 28.9784], 16);
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            }).addTo(map);

            var routeLayer = L.layerGroup().addTo(map);
            var obstacleLayer = L.layerGroup().addTo(map);
            var currentMarker, targetMarker;
            var currentBounds = null;

            // Add legend
            var legend = L.control({position: 'bottomright'});
            legend.onAdd = function (map) {
                var div = L.DomUtil.create('div', 'info legend');
                div.innerHTML += '<i style="background: blue"></i> Route<br>';
                div.innerHTML += '<i style="background: red"></i> Obstacle<br>';
                div.innerHTML += '<i>📍</i> Current Location<br>';
                div.innerHTML += '<i>🎯</i> Target Location<br>';
                return div;
            };
            legend.addTo(map);

            function updateMap() {
                fetch('/update')
                    .then(response => {
                        if (!response.ok) {
                            throw new Error(`HTTP error! status: ${response.status}`);
                        }
                        return response.json();
                    })
                    .then(data => {
                        console.log('Received data:', data);
                        if (data.error) {
                            throw new Error(data.error);
                        }
                        if (data.route && data.route.length > 0) {
                            routeLayer.clearLayers();
                            L.polyline(data.route, {color: 'blue', weight: 5}).addTo(routeLayer);
                            
                            if (!currentBounds || !currentBounds.contains(L.polyline(data.route).getBounds())) {
                                map.fitBounds(L.polyline(data.route).getBounds());
                                currentBounds = L.polyline(data.route).getBounds();
                            }
                        }
                        if (data.current_location) {
                            if (currentMarker) {
                                currentMarker.setLatLng(data.current_location);
                            } else {
                                currentMarker = L.marker(data.current_location, {icon: L.divIcon({className: 'current-location', html: '📍', iconSize: [30, 30]})}).addTo(map);
                            }
                            map.panTo(data.current_location);
                        }
                        if (data.target_location) {
                            if (targetMarker) {
                                targetMarker.setLatLng(data.target_location);
                            } else {
                                targetMarker = L.marker(data.target_location, {icon: L.divIcon({className: 'target-location', html: '🎯', iconSize: [30, 30]})}).addTo(map);
                            }
                        }
                        if (data.obstacles) {
                            obstacleLayer.clearLayers();
                            data.obstacles.forEach(obstacle => {
                                L.circleMarker(obstacle, {color: 'red', fillColor: 'red', fillOpacity: 0.5, radius: 10}).addTo(obstacleLayer);
                            });
                        }
                        if (data.accessibility_info) {
                            document.getElementById('accessibility').innerHTML = '<h3>Accessibility Info:</h3><ul>' + 
                                data.accessibility_info.map(info => `<li>${info}</li>`).join('') + '</ul>';
                        }
                        document.getElementById('status').innerHTML = `<h3>Navigation Status:</h3>
                            <p>Current Location: ${data.current_location.map(coord => coord.toFixed(4)).join(', ')}</p>
                            <p>Target: ${data.target_location.map(coord => coord.toFixed(4)).join(', ')}</p>
                            <p>Obstacles: ${data.obstacles.length}</p>`;

                        // Update metrics
                        if (data.metrics) {
                            document.getElementById('total-distance').textContent = data.metrics.total_distance;
                            document.getElementById('obstacles-avoided').textContent = data.metrics.total_obstacles_avoided;
                            document.getElementById('accessibility-score').textContent = data.metrics.average_accessibility_score.toFixed(2);
                            document.getElementById('route-changes').textContent = data.metrics.route_changes;
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        document.getElementById('status').innerHTML = '<h3>Error:</h3><p>' + error.message + '</p>';
                        document.getElementById('accessibility').innerHTML = '<h3>Error:</h3><p>' + error.message + '</p>';
                    });
            }

            updateMap();
            setInterval(updateMap, 1000);
        </script>
    </body>
    </html>
    ''')

@app.route('/update')
def update():
    global current_location, target_location, route, obstacles, graph
    global total_distance, total_obstacles_avoided, average_accessibility_score, route_changes
    try:
        if current_location is None or graph is None:
            raise ValueError("Navigation not initialized")
        
        accessibility_info = get_accessibility_info(current_location)
        
        data = {
            'current_location': current_location,
            'target_location': target_location,
            'route': route,
            'obstacles': obstacles,
            'accessibility_info': accessibility_info,
            'metrics': {
                'total_distance': round(total_distance, 2),
                'total_obstacles_avoided': total_obstacles_avoided,
                'average_accessibility_score': round(average_accessibility_score, 2),
                'route_changes': route_changes
            }
        }
        return jsonify(data)
    except Exception as e:
        print(f"Error in update route: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

def get_accessibility_info(location):
    if graph is None:
        return ["Graph not initialized"]
    try:
        node = ox.nearest_nodes(graph, location[1], location[0])
        tags = graph.nodes[node]
        info = []
        if tags.get('tactile_paving') == 'yes': info.append("Tactile paving present")
        if tags.get('sidewalk') in ['left', 'right', 'both']: info.append(f"Sidewalk: {tags['sidewalk']}")
        if tags.get('highway') == 'crossing': info.append(f"Crossing: {tags.get('crossing', 'unmarked')}")
        if tags.get('kerb') == 'lowered' or tags.get('curb_ramp') == 'yes': info.append("Curb ramp present")
        if tags.get('surface'): info.append(f"Surface: {tags['surface']}")
        if tags.get('lit') == 'yes': info.append("Well-lit area")
        return info
    except Exception as e:
        print(f"Error in get_accessibility_info: {str(e)}")
        return [f"Error: {str(e)}"]

def run_flask():
    app.run(debug=False, use_reloader=False)

def simulation():
    global current_location, target_location, route, obstacles
    global total_distance, total_obstacles_avoided, average_accessibility_score, route_changes

    route = get_route(current_location, target_location)
    print(f"Initial route calculated: {len(route)} points")

    step = 0
    total_accessibility = 0
    move_interval = 5  # Move every 5 iterations to slow down
    iteration = 0

    while True:
        iteration += 1
        if iteration % move_interval == 0 and step < len(route):
            prev_location = current_location
            current_location = route[step]
            step += 1

            total_distance += ox.distance.great_circle(prev_location[0], prev_location[1], 
                                                       current_location[0], current_location[1])

            node = ox.nearest_nodes(graph, current_location[1], current_location[0])
            accessibility = get_node_accessibility(graph.nodes[node])
            total_accessibility += accessibility
            average_accessibility_score = total_accessibility / step

            if detect_obstacles(current_location):
                total_obstacles_avoided += 1
                print(f"Obstacles detected: {len(obstacles)}. Recalculating route...")
                new_route = create_alternative_route(current_location, target_location, obstacles)
                if new_route != route:
                    route = new_route
                    route_changes += 1
                    print(f"New route calculated: {len(route)} points")
                    step = 0

        if step >= len(route):
            print("Destination reached!")
            # Reset the simulation
            current_location = (41.0082, 28.9784)  # Reset to start location
            obstacles.clear()
            route = get_route(current_location, target_location)
            step = 0
            total_accessibility = 0
            # Reset metrics for the new simulation run
            total_distance = 0
            total_obstacles_avoided = 0
            average_accessibility_score = 1.0
            route_changes = 0

        time.sleep(0.2)  # Reduced sleep time for smoother updates, but still slower than before

        # Print current status for debugging
        if iteration % move_interval == 0:
            print(f"Step: {step}, Location: {current_location}, Distance: {total_distance:.2f}")

def main():
    initialize_graph()
    flask_thread = Thread(target=run_flask)
    simulation_thread = Thread(target=simulation)
    
    flask_thread.start()
    simulation_thread.start()
    
    flask_thread.join()
    simulation_thread.join()

if __name__ == "__main__":
    main()
