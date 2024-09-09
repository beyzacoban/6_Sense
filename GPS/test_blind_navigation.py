import unittest
from unittest.mock import patch, MagicMock
import networkx as nx
from gps import get_node_accessibility, get_route, create_alternative_route

class TestBlindNavigation(unittest.TestCase):

    def setUp(self):
        # Create a sample graph for testing
        self.graph = nx.Graph()
        self.graph.add_node(1, y=40.7128, x=-74.0060, tactile_paving='yes', sidewalk='both')
        self.graph.add_node(2, y=40.7129, x=-74.0061, highway='crossing', crossing='traffic_signals')
        self.graph.add_node(3, y=40.7130, x=-74.0062, kerb='lowered', surface='asphalt', lit='yes')
        self.graph.add_edge(1, 2)
        self.graph.add_edge(2, 3)

    def test_get_node_accessibility(self):
        accessibility = get_node_accessibility(1, self.graph)
        self.assertLess(accessibility, 1.0)  # Accessibility should be improved (lower value)

    @patch('gps.ox.nearest_nodes')
    @patch('gps.nx.shortest_path')
    def test_get_route(self, mock_shortest_path, mock_nearest_nodes):
        mock_graph = MagicMock()
        mock_graph.nodes = {
            1: {'y': 40.7128, 'x': -74.0060},
            2: {'y': 40.7129, 'x': -74.0061},
            3: {'y': 40.7130, 'x': -74.0062}
        }
        mock_nearest_nodes.side_effect = [1, 3]
        mock_shortest_path.return_value = [1, 2, 3]

        with patch('gps.graph', mock_graph):
            start = (40.7128, -74.0060)
            end = (40.7130, -74.0062)
            route = get_route(start, end)
            self.assertEqual(len(route), 3)  # Should find a route with 3 points

    @patch('gps.ox.nearest_nodes')
    @patch('gps.nx.shortest_path')
    def test_create_alternative_route(self, mock_shortest_path, mock_nearest_nodes):
        mock_graph = MagicMock()
        mock_graph.nodes = {
            1: {'y': 40.7128, 'x': -74.0060},
            2: {'y': 40.7129, 'x': -74.0061},
            3: {'y': 40.7130, 'x': -74.0062}
        }
        mock_nearest_nodes.side_effect = [1, 2, 3]
        mock_shortest_path.return_value = [1, 3]

        with patch('gps.graph', mock_graph):
            start = (40.7128, -74.0060)
            end = (40.7130, -74.0062)
            obstacles = [(40.7129, -74.0061)]  # Add an obstacle at node 2
            route = create_alternative_route(start, end, obstacles)
            self.assertIsNotNone(route)  # Should still find a route
            self.assertEqual(len(route), 2)  # Should find a route with 2 points (avoiding the obstacle)

if __name__ == '__main__':
    unittest.main()