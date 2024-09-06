import random
import time
from flask import Flask, render_template_string, jsonify
from threading import Thread
import osmnx as ox
import networkx as nx

app = Flask(__name__)

# Global değişkenler
current_location = None  # Mevcut konum
target_location = None   # Hedef konum
route = None             # Rota
graph = None             # Şehir haritası grafiği
obstacles = []           # Engeller listesi

# Belirli bir şehir merkezi (örneğin, New York City)
CITY_CENTER = (40.7128, -74.0060)

# Rota hesaplama fonksiyonu
def get_route(start, end):
    global graph
    start_node = ox.nearest_nodes(graph, start[1], start[0])
    end_node = ox.nearest_nodes(graph, end[1], end[0])
    route = nx.shortest_path(graph, start_node, end_node, weight='length')
    return [[graph.nodes[node]['y'], graph.nodes[node]['x']] for node in route]

# Engel tespit etme fonksiyonu (simülasyon)
def detect_obstacles(current_loc):
    # Engel tespitini simüle et
    if random.random() < 0.1:  # %10 ihtimalle yeni engel
        lat = current_loc[0] + random.uniform(-0.0005, 0.0005)
        lon = current_loc[1] + random.uniform(-0.0005, 0.0005)
        new_obstacle = (lat, lon)
        if new_obstacle not in obstacles:
            obstacles.append(new_obstacle)
            return True
    return False

# Alternatif rota oluşturma fonksiyonu
def create_alternative_route(start, end, obstacles):
    global graph
    temp_graph = graph.copy()
    for obstacle in obstacles:
        nearest_node = ox.nearest_nodes(temp_graph, obstacle[1], obstacle[0])
        if nearest_node in temp_graph:
            temp_graph.remove_node(nearest_node)
    start_node = ox.nearest_nodes(temp_graph, start[1], start[0])
    end_node = ox.nearest_nodes(temp_graph, end[1], end[0])
    try:
        route = nx.shortest_path(temp_graph, start_node, end_node, weight='length')
        return [[temp_graph.nodes[node]['y'], temp_graph.nodes[node]['x']] for node in route]
    except nx.NetworkXNoPath:
        print("Yol bulunamadı. Orijinal rotayı koruyoruz.")
        return get_route(start, end)

# Ana sayfa rotası
@app.route('/')
def index():
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>GPS Navigation with Obstacle Avoidance</title>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
        <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
        <style>
            #map { height: 600px; }
        </style>
    </head>
    <body>
        <div id="map"></div>
        <div id="status"></div>
        <script>
            var map = L.map('map').setView([40.7128, -74.0060], 14);
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            }).addTo(map);

            var routeLayer = L.layerGroup().addTo(map);
            var obstacleLayer = L.layerGroup().addTo(map);
            var currentMarker, targetMarker;

            function updateMap() {
                fetch('/update')
                    .then(response => response.json())
                    .then(data => {
                        console.log('Received data:', data);
                        if (data.route && data.route.length > 0) {
                            routeLayer.clearLayers();
                            L.polyline(data.route, {color: 'blue'}).addTo(routeLayer);
                            map.fitBounds(L.polyline(data.route).getBounds());
                        }
                        if (data.current_location) {
                            if (currentMarker) {
                                currentMarker.setLatLng(data.current_location);
                            } else {
                                currentMarker = L.marker(data.current_location, {icon: L.divIcon({className: 'current-location', html: '📍'})}).addTo(map);
                            }
                            map.panTo(data.current_location);
                        }
                        if (data.target_location) {
                            if (targetMarker) {
                                targetMarker.setLatLng(data.target_location);
                            } else {
                                targetMarker = L.marker(data.target_location, {icon: L.divIcon({className: 'target-location', html: '🎯'})}).addTo(map);
                            }
                        }
                        if (data.obstacles) {
                            obstacleLayer.clearLayers();
                            data.obstacles.forEach(obstacle => {
                                L.circleMarker(obstacle, {color: 'red', fillColor: 'red', fillOpacity: 0.5, radius: 10}).addTo(obstacleLayer);
                            });
                        }
                        document.getElementById('status').innerText = `Current Location: ${data.current_location}, Target: ${data.target_location}, Obstacles: ${data.obstacles.length}`;
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        document.getElementById('status').innerText = 'Error updating map';
                    });
            }

            updateMap();
            setInterval(updateMap, 1000);
        </script>
    </body>
    </html>
    ''')

# Güncelleme rotası
@app.route('/update')
def update():
    global current_location, target_location, route, obstacles
    return jsonify({
        'current_location': current_location,
        'target_location': target_location,
        'route': route,
        'obstacles': obstacles
    })

# Flask uygulamasını çalıştırma fonksiyonu
def run_flask():
    app.run(debug=False, use_reloader=False)

# Ana fonksiyon
def main():
    global current_location, target_location, route, graph, obstacles

    # Flask uygulamasını ayrı bir thread'de başlat
    Thread(target=run_flask).start()

    # Başlangıç ve hedef konumlarını ayarla
    current_location = (40.7128, -74.0060)  # New York City Merkezi
    target_location = (40.7484, -73.9857)   # Empire State Binası
    print(f"Başlangıç konumu: {current_location}")
    print(f"Hedef konum: {target_location}")

    # Bölge için grafik oluştur
    graph = ox.graph_from_point(current_location, dist=5000, network_type='walk')
    print("Grafik oluşturuldu.")

    # İlk rotayı hesapla
    route = get_route(current_location, target_location)
    print(f"İlk rota hesaplandı: {len(route)} nokta")

    step = 0
    while True:
        # Rota boyunca hareket et
        if step < len(route):
            current_location = route[step]
            step += 1
        else:
            print("Hedefe ulaşıldı!")
            break

        print(f"Mevcut Konum: {current_location}")

        # Engel tespiti yap ve gerekirse rotayı yeniden hesapla
        if detect_obstacles(current_location):
            print(f"Engeller tespit edildi: {len(obstacles)}. Rota yeniden hesaplanıyor...")
            new_route = create_alternative_route(current_location, target_location, obstacles)
            if new_route != route:
                route = new_route
                print(f"Yeni rota hesaplandı: {len(route)} nokta")
                step = 0  # Adımı yeni rotanın başlangıcına sıfırla

        time.sleep(1)

if __name__ == "__main__":
    main()


# Test Süreci Açıklaması (Kullanılan Teknolojiler ve Kütüphaneler):
# 1. Program başlatılır ve Flask web uygulaması ayrı bir thread'de çalıştırılır.
#    - Flask: Web uygulaması için kullanılan micro web framework
#    - threading: Çoklu iş parçacığı yönetimi için kullanılan Python modülü
# 2. Başlangıç ve hedef konumları belirlenir (New York City merkezi ve Empire State Binası).
#    - Koordinatlar: Enlem ve boylam değerleri kullanılır
# 3. Şehir haritası için bir graf oluşturulur.
#    - OSMnx: OpenStreetMap verilerinden graf oluşturmak için kullanılan kütüphane
# 4. İlk rota hesaplanır.
#    - NetworkX: Graf üzerinde en kısa yol algoritmaları için kullanılan kütüphane
# 5. Simülasyon döngüsü başlar:
#    a. Mevcut konum güncellenir (rota üzerinde ilerleme).
#    b. Her adımda, engel tespit etme olasılığı kontrol edilir.
#       - Random: Rastgele engel oluşturmak için kullanılan Python modülü
#    c. Engel tespit edilirse, yeni bir rota hesaplanır.
#    d. Yeni rota, mevcut engelleri göz önünde bulundurarak oluşturulur.
#       - NetworkX: Alternatif rota hesaplamak için tekrar kullanılır
# 6. Bu süreç, hedef konuma ulaşılana kadar devam eder.
#    - time: Simülasyon adımları arasında bekleme süresi için kullanılan Python modülü
# Not: Gerçek zamanlı GPS verisi ve gerçek engel tespiti yerine simülasyon kullanılmaktadır.
