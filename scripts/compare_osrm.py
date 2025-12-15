"""
Script to compare py-osrm-backend routing with official OSRM demo server.

Usage:
    python scripts/compare_osrm.py
"""

import sys
import os
import requests
import json

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from osrm.extractor.graph_builder import GraphBuilder
from osrm.engine.dijkstra import DijkstraEngine
from osrm.structures.graph import haversine_distance


def find_nearest_node(graph, lat, lon):
    """Find nearest routable node to given coordinates."""
    nearest = None
    min_dist = float('inf')
    for node_id, node in graph.nodes.items():
        # Only consider nodes that have outgoing edges (are routable)
        if node_id not in graph.adj_list or len(graph.adj_list[node_id]) == 0:
            continue
        d = (node.lat - lat)**2 + (node.lon - lon)**2
        if d < min_dist:
            min_dist = d
            nearest = node
    return nearest


def query_official_osrm(start_lon, start_lat, end_lon, end_lat):
    """Query the official OSRM demo server."""
    url = f"https://router.project-osrm.org/route/v1/driving/{start_lon},{start_lat};{end_lon},{end_lat}?overview=false"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        if data.get('code') == 'Ok' and data.get('routes'):
            route = data['routes'][0]
            return {
                'distance': route['distance'] / 1000,  # Convert m to km
                'duration': route['duration'] / 60,    # Convert s to min
                'status': 'Ok'
            }
        return {'status': data.get('code', 'Error'), 'distance': None}
    except Exception as e:
        return {'status': f'Error: {e}', 'distance': None}


def main():
    # Monaco coordinates for testing
    # Start: Casino de Monte-Carlo
    start_lat, start_lon = 43.7396, 7.4275
    # End: Port Hercule
    end_lat, end_lon = 43.7350, 7.4200
    
    print("=" * 60)
    print("py-osrm-backend vs Official OSRM Comparison")
    print("=" * 60)
    print(f"\nRoute: Casino Monte-Carlo -> Port Hercule")
    print(f"Start: ({start_lat}, {start_lon})")
    print(f"End:   ({end_lat}, {end_lon})")
    print()
    
    # 1. Query official OSRM
    print("Querying official OSRM server...")
    official = query_official_osrm(start_lon, start_lat, end_lon, end_lat)
    if official['status'] == 'Ok':
        print(f"  Distance: {official['distance']:.3f} km")
        print(f"  Duration: {official['duration']:.1f} min")
    else:
        print(f"  Status: {official['status']}")
    
    # 2. Build graph from Monaco PBF
    print("\nBuilding graph from Monaco PBF...")
    pbf_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'monaco-latest.osm.pbf')
    
    if not os.path.exists(pbf_path):
        print(f"ERROR: Monaco PBF not found at {pbf_path}")
        print("Download it first with:")
        print("  Invoke-WebRequest -Uri 'https://download.geofabrik.de/europe/monaco-latest.osm.pbf' -OutFile 'data/monaco-latest.osm.pbf'")
        return
    
    builder = GraphBuilder()
    graph = builder.build_graph(pbf_path)
    
    # 3. Find nearest nodes
    start_node = find_nearest_node(graph, start_lat, start_lon)
    end_node = find_nearest_node(graph, end_lat, end_lon)
    
    if not start_node or not end_node:
        print("ERROR: Could not find nodes near coordinates")
        return
    
    print(f"\nNearest nodes found:")
    print(f"  Start: Node {start_node.id} at ({start_node.lat:.4f}, {start_node.lon:.4f})")
    print(f"  End:   Node {end_node.id} at ({end_node.lat:.4f}, {end_node.lon:.4f})")
    
    # 4. Route with Dijkstra
    print("\nRouting with Dijkstra...")
    engine = DijkstraEngine(graph)
    
    print(f"  Start node has {len(graph.adj_list.get(start_node.id, []))} outgoing edges")
    print(f"  End node has {len(graph.adj_list.get(end_node.id, []))} outgoing edges")
    
    distance, path = engine.shortest_path(start_node.id, end_node.id)
    
    if path:
        print(f"  Distance: {distance:.3f} km")
        print(f"  Path nodes: {len(path)}")
        our_result = distance
    else:
        print("  No route found!")
        our_result = None
    
    # 5. Comparison
    print("\n" + "=" * 60)
    print("COMPARISON")
    print("=" * 60)
    if official['status'] == 'Ok' and our_result is not None:
        diff = abs(official['distance'] - our_result)
        diff_pct = (diff / official['distance']) * 100 if official['distance'] > 0 else 0
        print(f"Official OSRM distance: {official['distance']:.3f} km")
        print(f"py-osrm-backend distance: {our_result:.3f} km")
        print(f"Difference: {diff:.3f} km ({diff_pct:.1f}%)")
        
        if diff_pct < 10:
            print("\n✅ Results are similar (within 10%)")
        else:
            print("\n⚠️ Significant difference - this is expected due to:")
            print("   - Different graph extraction")
            print("   - No speed/traffic weighting")
            print("   - Simplified one-way handling")
    else:
        print(f"Official status: {official['status']}")
        print(f"Our result: {our_result}")
        print("Could not compare - one or both queries failed")


if __name__ == '__main__':
    main()
