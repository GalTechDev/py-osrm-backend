import unittest
import sys
import os
import math
import random

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from osrm.structures.graph import Graph
from osrm.engine.contraction_hierarchies import ContractionHierarchies
from osrm.engine.dijkstra import DijkstraEngine

class TestContractionHierarchies(unittest.TestCase):
    
    def setUp(self):
        """Create a simple test graph:
           1 --2--> 2 --3--> 3
           |                 ^
           +-------6---------+
        """
        self.graph = Graph()
        self.graph.add_node(1, 0, 0)
        self.graph.add_node(2, 0, 1)
        self.graph.add_node(3, 0, 2)
        
        # Bidirectional edges for CH
        self.graph.add_edge(1, 2, 2.0)
        self.graph.add_edge(2, 1, 2.0)
        self.graph.add_edge(2, 3, 3.0)
        self.graph.add_edge(3, 2, 3.0)
        self.graph.add_edge(1, 3, 6.0)
        self.graph.add_edge(3, 1, 6.0)

    def test_preprocessing(self):
        ch = ContractionHierarchies(self.graph)
        ch.preprocess()
        
        # All nodes should be contracted
        for node in ch.ch_nodes.values():
            self.assertTrue(node.contracted)
    
    def test_query_shortest_path(self):
        ch = ContractionHierarchies(self.graph)
        ch.preprocess()
        
        dist, path = ch.query(1, 3)
        # Shortest is 1->2->3 = 5
        self.assertEqual(dist, 5.0)
        self.assertIn(1, path)
        self.assertIn(3, path)

    def test_preprocess_does_not_modify_graph(self):
        edges_before = {n: list(e) for n, e in self.graph.adj_list.items()}
        ch = ContractionHierarchies(self.graph)
        ch.preprocess()
        self.assertEqual(self.graph.adj_list, edges_before)

    def test_path_is_unpacked(self):
        ch = ContractionHierarchies(self.graph)
        ch.preprocess()
        _, path = ch.query(1, 3)
        self.assertEqual(path, [1, 2, 3])

    def test_matches_dijkstra_on_random_graphs(self):
        rng = random.Random(42)
        for _ in range(20):
            graph = Graph()
            n = rng.randint(5, 30)
            for i in range(n):
                graph.add_node(i, 0, 0)
            for _ in range(n * 3):
                u, v = rng.randrange(n), rng.randrange(n)
                if u != v:
                    graph.add_edge(u, v, float(rng.randint(1, 20)))

            dijkstra = DijkstraEngine(graph)
            ch = ContractionHierarchies(graph)
            ch.preprocess()

            for _ in range(20):
                s, t = rng.randrange(n), rng.randrange(n)
                expected, _ = dijkstra.shortest_path(s, t)
                dist, path = ch.query(s, t)
                self.assertEqual(dist, expected)
                if math.isinf(expected):
                    self.assertEqual(path, [])
                    continue
                # The unpacked path only uses original edges and has the right length
                self.assertEqual((path[0], path[-1]), (s, t))
                length = sum(
                    min(e.weight for e in graph.get_edges(a) if e.target == b)
                    for a, b in zip(path, path[1:])
                )
                self.assertAlmostEqual(length, dist)

if __name__ == '__main__':
    unittest.main()
