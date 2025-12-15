"""
Debug script to check graph connectivity.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from osrm.extractor.graph_builder import GraphBuilder


def main():
    # Point to the data file used by the server
    pbf_path = os.path.join(os.path.dirname(__file__), '..', 'src', 'data', 'new-caledonia-251208.osm.pbf')
    if not os.path.exists(pbf_path):
        # Fallback/Search
        pbf_path = "c:/Users/moreaum/Documents/Code/Programme/osrm/py-osrm-backend/src/data/new-caledonia-251208.osm.pbf"
    
    print(f"Analyzing {pbf_path}...")
    
    print("Building graph...")
    builder = GraphBuilder()
    graph = builder.build_graph(pbf_path)
    
    print(f"\nGraph Statistics:")
    print(f"  Nodes: {len(graph.nodes)}")
    
    total_edges = sum(len(edges) for edges in graph.adj_list.values())
    print(f"  Edges: {total_edges}")
    
    # Check connectivity
    nodes_with_edges = sum(1 for edges in graph.adj_list.values() if len(edges) > 0)
    print(f"  Nodes with outgoing edges: {nodes_with_edges}")
    
    # Sample some edges
    print("\nSample edges:")
    count = 0
    for node_id, edges in graph.adj_list.items():
        for edge in edges:
            print(f"  {node_id} -> {edge.target} ({edge.weight:.4f} km)")
            count += 1
            if count >= 5:
                break
        if count >= 5:
            break


if __name__ == '__main__':
    main()
