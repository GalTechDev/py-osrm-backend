"""
Test routing with nodes that we know are connected.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
import requests
from osrm.extractor.graph_builder import GraphBuilder
from osrm.engine.dijkstra import DijkstraEngine

pbf = os.path.join(os.path.dirname(__file__), '..', 'data', 'monaco-latest.osm.pbf')
print("Building graph...")
builder = GraphBuilder()
graph = builder.build_graph(pbf)

# Find connected component with most edges (main road network)
nodes_with_edges = [(n, len(e)) for n, e in graph.adj_list.items() if len(e) > 0]
nodes_with_edges.sort(key=lambda x: -x[1])  # Sort by edge count (hubs first)

# Pick start from a "hub" node
start_id = nodes_with_edges[0][0]
start_node = graph.nodes[start_id]

# Find end by traversing 10+ hops from start
visited = set()
current = start_id
for _ in range(10):
    edges = graph.adj_list.get(current, [])
    if not edges:
        break
    # Pick unvisited neighbor
    for e in edges:
        if e.target not in visited:
            visited.add(current)
            current = e.target
            break

end_id = current
end_node = graph.nodes[end_id]

print(f"\nStart: Node {start_id} at ({start_node.lat:.4f}, {start_node.lon:.4f})")
print(f"End:   Node {end_id} at ({end_node.lat:.4f}, {end_node.lon:.4f})")

# Route
engine = DijkstraEngine(graph)
dist, path = engine.shortest_path(start_id, end_id)
print(f"\npy-osrm-backend: dist={dist:.3f} km, path length={len(path)}")

# Compare with official
url = f"https://router.project-osrm.org/route/v1/driving/{start_node.lon},{start_node.lat};{end_node.lon},{end_node.lat}?overview=false"
try:
    r = requests.get(url, timeout=10)
    data = r.json()
    if data.get('code') == 'Ok':
        official_dist = data['routes'][0]['distance'] / 1000
        print(f"Official OSRM:   dist={official_dist:.3f} km")
        diff = abs(dist - official_dist)
        print(f"\nDifference: {diff:.3f} km ({diff/official_dist*100:.1f}%)")
except Exception as e:
    print(f"OSRM request failed: {e}")
