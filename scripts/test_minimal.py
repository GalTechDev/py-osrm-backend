"""Minimal routing test."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from osrm.extractor.graph_builder import GraphBuilder
from osrm.engine.dijkstra import DijkstraEngine

pbf = os.path.join(os.path.dirname(__file__), '..', 'data', 'monaco-latest.osm.pbf')
builder = GraphBuilder()
graph = builder.build_graph(pbf)

# Count edges
edges = sum(len(e) for e in graph.adj_list.values())
nodes_with_edges = [n for n, e in graph.adj_list.items() if len(e) > 0]
print(f"Nodes: {len(graph.nodes)}, Edges: {edges}, Routable: {len(nodes_with_edges)}")

# Pick two connected nodes
if nodes_with_edges:
    start = nodes_with_edges[0]
    # Find a node reachable from start
    end = None
    if graph.adj_list[start]:
        end = graph.adj_list[start][0].target
    
    if end:
        print(f"Testing: {start} -> {end}")
        engine = DijkstraEngine(graph)
        dist, path = engine.shortest_path(start, end)
        print(f"Result: dist={dist}, path={path}")
