"""
Check connectivity for specific coordinates in New Caledonia.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from osrm.extractor.graph_builder import GraphBuilder
from osrm.engine.dijkstra import DijkstraEngine

# Coords from user request (lon, lat)
POINTS = [
    (166.4416, -22.2711),
    (164.8658, -21.0595),
    (164.2833, -20.5667)
]

def main():
    pbf_path = "c:/Users/moreaum/Documents/Code/Programme/osrm/py-osrm-backend/src/data/new-caledonia-251208.osm.pbf"
    
    print(f"Building graph from {pbf_path}...")
    builder = GraphBuilder()
    graph = builder.build_graph(pbf_path)
    
    # 1. Snap points to nodes
    nodes = []
    for lon, lat in POINTS:
        nearest = None
        min_dist = float('inf')
        for node in graph.nodes.values():
            d = (node.lat - lat)**2 + (node.lon - lon)**2
            if d < min_dist:
                min_dist = d
                nearest = node
        nodes.append(nearest)
        
    for i, node in enumerate(nodes):
        print(f"Point {i}: {POINTS[i]} snapped to Node {node.id} ({node.lat}, {node.lon})")
        # Check outgoing edges
        edges = graph.get_edges(node.id)
        print(f"  Outgoing edges: {len(edges)}")
        if edges:
            print(f"  First edge target: {edges[0].target}")

    # 2. Check path
    engine = DijkstraEngine(graph)
    
    # Check 0 -> 1
    dist, path = engine.shortest_path(nodes[0].id, nodes[1].id)
    print(f"\nPath 0->1: dist={dist}, path_len={len(path)}")
    
    # Check 1 -> 2
    dist2, path2 = engine.shortest_path(nodes[1].id, nodes[2].id)
    print(f"\nPath 1->2: dist={dist2}, path_len={len(path2)}")

if __name__ == '__main__':
    main()
