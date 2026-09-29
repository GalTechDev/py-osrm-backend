from flask import Flask, request, jsonify
from ..extractor.graph_builder import GraphBuilder
from ..engine.dijkstra import DijkstraEngine
import os

app = Flask(__name__)
graph = None
engine = None

# Rough travel speed used for durations (50 km/h), until speed profiles exist
AVERAGE_SPEED_MPS = 13.8

def init_app(osm_file_path: str):
    global graph, engine
    if not os.path.exists(osm_file_path):
        raise FileNotFoundError(f"OSM file not found: {osm_file_path}")
    
    print("Initializing Graph...")
    builder = GraphBuilder()
    graph = builder.build_graph(osm_file_path)
    engine = DijkstraEngine(graph)
    print("Initialization complete.")

@app.route('/health')
def health():
    if graph is None:
        return jsonify({'status': 'initializing'}), 503
    return jsonify({'status': 'ok', 'nodes': len(graph)})

@app.route('/route/v1/driving/<coords>')
def route(coords):
    # Expected format: lon1,lat1;lon2,lat2
    # This is a simplified OSRM-like endpoint
    try:
        parts = coords.split(';')
        if len(parts) < 2:
            return jsonify({'code': 'InvalidRequest', 'message': 'At least two coordinates required'}), 400
        
        waypoints = []
        for part in parts:
            try:
                lon, lat = map(float, part.split(','))
                node = _find_nearest_node(lat, lon)
                if not node:
                     return jsonify({'code': 'NoSegment', 'message': f'Could not find node near {lat},{lon}'}), 400
                waypoints.append(node)
            except ValueError:
                return jsonify({'code': 'InvalidRequest', 'message': 'Coordinates must be lon,lat'}), 400

        total_dist = 0.0
        full_path_ids = []

        for i in range(len(waypoints) - 1):
            start_node = waypoints[i]
            end_node = waypoints[i+1]
            
            dist, path = engine.shortest_path(start_node.id, end_node.id)
            
            if not path:
                 return jsonify({'code': 'NoRoute', 'message': 'No route found between waypoints'}), 404
            
            total_dist += dist
            
            # Append path (avoid duplicating the connection node)
            if i > 0:
                full_path_ids.extend(path[1:])
            else:
                full_path_ids.extend(path)

        # OSRM units: metres and seconds
        distance_m = total_dist * 1000
        return jsonify({
            'code': 'Ok',
            'routes': [{
                'distance': distance_m,
                'duration': distance_m / AVERAGE_SPEED_MPS,
                'geometry': _encode_path_geometry(full_path_ids)
            }]
        })

    except Exception as e:
        return jsonify({'code': 'Error', 'message': str(e)}), 500

def _find_nearest_node(lat, lon):
    # O(N) naive search over routable nodes
    routable = _routable_nodes()
    nearest = None
    min_dist = float('inf')
    
    for node_id, node in graph.nodes.items():
        if node_id not in routable:
            continue

        d = (node.lat - lat)**2 + (node.lon - lon)**2
        if d < min_dist:
            min_dist = d
            nearest = node
    return nearest

_routable_cache = (None, set())

def _routable_nodes():
    """Nodes touched by at least one edge, in either direction (cached per graph)."""
    global _routable_cache
    cached_graph, nodes = _routable_cache
    if cached_graph is not graph:
        nodes = set()
        for source, edges in graph.adj_list.items():
            for edge in edges:
                nodes.add(source)
                nodes.add(edge.target)
        _routable_cache = (graph, nodes)
    return nodes

def _encode_path_geometry(path_ids):
    # Return list of [lon, lat] for simplicity
    coords = []
    for nid in path_ids:
        node = graph.get_node(nid)
        coords.append([node.lon, node.lat])
    return {'type': 'LineString', 'coordinates': coords}

if __name__ == '__main__':
    # Default to a sample file or env var
    osm_path = os.environ.get('OSRM_FILE', 'data.osm')
    init_app(osm_path)
    app.run(
        host=os.environ.get('OSRM_HOST', '127.0.0.1'),
        port=int(os.environ.get('OSRM_PORT', '5000')),
        debug=os.environ.get('FLASK_DEBUG') == '1',
    )
