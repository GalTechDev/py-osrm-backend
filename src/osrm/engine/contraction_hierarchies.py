"""
Contraction Hierarchies (CH) implementation.

CH is a speed-up technique for shortest path queries:
1. Preprocessing: Contract nodes in order of importance, adding shortcuts
2. Query: Bidirectional Dijkstra on the augmented graph (upward searches only)
"""

import heapq
from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass, field
from ..structures.graph import Graph, Edge, haversine_distance

@dataclass
class CHNode:
    """Node with contraction hierarchy level."""
    id: int
    level: int = 0  # Higher = more important
    contracted: bool = False

@dataclass
class Shortcut:
    """A shortcut edge bypassing a contracted node."""
    source: int
    target: int
    weight: float
    via: int  # The contracted node this shortcut bypasses

@dataclass
class ShortcutEdge(Edge):
    """Graph edge standing for a shortcut, so query paths can be unpacked."""
    via: int = -1

class ContractionHierarchies:
    """
    Contraction Hierarchies for fast shortest path queries.
    
    Usage:
        ch = ContractionHierarchies(graph)
        ch.preprocess()
        distance, path = ch.query(start, end)
    """
    
    # Max nodes settled by a witness search before giving up and adding the shortcut
    WITNESS_SEARCH_LIMIT = 500
    
    def __init__(self, graph: Graph):
        self.original_graph = graph
        self.ch_nodes: Dict[int, CHNode] = {}
        # Private copy of the edges (original + shortcuts): the input graph is never modified
        self.out_edges: Dict[int, List[Edge]] = {}
        self.in_edges: Dict[int, List[Edge]] = {}
        self.upward_edges: Dict[int, List[Edge]] = {}  # Edges to higher-level nodes
        self.downward_edges: Dict[int, List[Edge]] = {}  # Edges to lower-level nodes
        # Reverse upward edges: for v, edges u -> v where u is higher than v (backward search)
        self.backward_upward_edges: Dict[int, List[Edge]] = {}
        self.shortcuts: List[Shortcut] = []
        self._initialize()
    
    def _initialize(self):
        """Initialize CH nodes and edge copies from the original graph."""
        for node_id in self.original_graph.nodes:
            self.ch_nodes[node_id] = CHNode(id=node_id)
            self.out_edges[node_id] = []
            self.in_edges[node_id] = []
            self.upward_edges[node_id] = []
            self.downward_edges[node_id] = []
            self.backward_upward_edges[node_id] = []
        for edges in self.original_graph.adj_list.values():
            for edge in edges:
                self.out_edges[edge.source].append(edge)
                self.in_edges[edge.target].append(edge)
    
    def _compute_node_importance(self, node_id: int, contracted: Set[int]) -> int:
        """
        Compute importance of a node for contraction ordering.
        Lower importance = contract first.
        
        Simplified heuristic: edge difference + contracted neighbors
        """
        # Count edges to/from non-contracted neighbors
        in_edges = 0
        out_edges = 0
        contracted_neighbors = 0
        
        for edge in self.out_edges[node_id]:
            if edge.target in contracted:
                contracted_neighbors += 1
            else:
                out_edges += 1
        
        for edge in self.in_edges[node_id]:
            if edge.source in contracted:
                contracted_neighbors += 1
            else:
                in_edges += 1
        
        # Shortcuts needed = in_edges * out_edges (worst case)
        shortcuts_needed = in_edges * out_edges
        
        # Edge difference = shortcuts added - edges removed
        edge_diff = shortcuts_needed - (in_edges + out_edges)
        
        # Contracted neighbors penalty spreads contraction evenly over the graph
        return edge_diff + contracted_neighbors
    
    def preprocess(self, max_nodes: int = None):
        """
        Contract nodes in order of importance.
        
        Args:
            max_nodes: Limit preprocessing to first N nodes (for testing)
        """
        print("CH Preprocessing: Computing contraction order...")
        contracted: Set[int] = set()
        node_ids = list(self.original_graph.nodes.keys())
        
        if max_nodes:
            node_ids = node_ids[:max_nodes]
        
        # Priority queue: (importance, node_id)
        pq = []
        for node_id in node_ids:
            importance = self._compute_node_importance(node_id, contracted)
            heapq.heappush(pq, (importance, node_id))
        
        level = 0
        total = len(node_ids)
        
        while pq:
            _, node_id = heapq.heappop(pq)
            
            if node_id in contracted:
                continue
            
            # Lazy update: recompute importance
            new_importance = self._compute_node_importance(node_id, contracted)
            if pq and new_importance > pq[0][0]:
                heapq.heappush(pq, (new_importance, node_id))
                continue
            
            # Contract this node
            self._contract_node(node_id, contracted)
            self.ch_nodes[node_id].level = level
            self.ch_nodes[node_id].contracted = True
            contracted.add(node_id)
            level += 1
            
            if level % 100 == 0:
                print(f"  Contracted {level}/{total} nodes...")
        
        # Build upward/downward edge lists
        self._build_ch_graph()
        print(f"CH Preprocessing complete. {len(self.shortcuts)} shortcuts created.")
    
    def _contract_node(self, node_id: int, contracted: Set[int]):
        """Contract a node by adding necessary shortcuts."""
        # Find incoming edges from non-contracted nodes
        incoming = [
            (edge.source, edge.weight) for edge in self.in_edges[node_id]
            if edge.source not in contracted and edge.source != node_id
        ]
        
        # Find outgoing edges to non-contracted nodes
        outgoing = [
            (edge.target, edge.weight) for edge in self.out_edges[node_id]
            if edge.target not in contracted and edge.target != node_id
        ]
        
        if not incoming or not outgoing:
            return
        max_out = max(w for _, w in outgoing)
        
        # Add shortcuts if needed
        for u, w_in in incoming:
            witness = self._witness_search(u, node_id, contracted, w_in + max_out)
            for v, w_out in outgoing:
                if u == v:
                    continue
                
                shortcut_weight = w_in + w_out
                
                # Shortcut unnecessary if a path u -> v avoiding node_id is as short
                if witness.get(v, float('inf')) <= shortcut_weight:
                    continue
                
                shortcut = Shortcut(u, v, shortcut_weight, node_id)
                self.shortcuts.append(shortcut)
                
                edge = ShortcutEdge(u, v, shortcut_weight, f"shortcut_via_{node_id}", via=node_id)
                self.out_edges[u].append(edge)
                self.in_edges[v].append(edge)
    
    def _witness_search(self, source: int, excluded: int, contracted: Set[int],
                        max_dist: float) -> Dict[int, float]:
        """
        Dijkstra from source over non-contracted nodes, skipping `excluded`,
        bounded by max_dist and WITNESS_SEARCH_LIMIT settled nodes.
        Stopping early only adds unneeded shortcuts, never wrong ones.
        """
        dist: Dict[int, float] = {source: 0.0}
        pq = [(0.0, source)]
        settled = 0
        while pq and settled < self.WITNESS_SEARCH_LIMIT:
            d, u = heapq.heappop(pq)
            if d > dist.get(u, float('inf')) or d > max_dist:
                continue
            settled += 1
            for edge in self.out_edges[u]:
                v = edge.target
                if v == excluded or v in contracted:
                    continue
                new_dist = d + edge.weight
                if new_dist < dist.get(v, float('inf')):
                    dist[v] = new_dist
                    heapq.heappush(pq, (new_dist, v))
        return dist
    
    def _build_ch_graph(self):
        """Build upward and downward edge lists based on node levels."""
        # Include original edges + shortcuts
        for edges in self.out_edges.values():
            for edge in edges:
                src_level = self.ch_nodes[edge.source].level
                tgt_level = self.ch_nodes[edge.target].level
                
                if tgt_level > src_level:
                    self.upward_edges[edge.source].append(edge)
                else:
                    self.downward_edges[edge.source].append(edge)
                    self.backward_upward_edges[edge.target].append(edge)
    
    def query(self, start: int, end: int) -> Tuple[float, List[int]]:
        """
        Bidirectional Dijkstra query on CH graph.
        
        Returns (distance, path).
        """
        if start not in self.ch_nodes or end not in self.ch_nodes:
            raise ValueError("Start or end node not in graph")
        
        # Forward search (upward from start)
        dist_forward: Dict[int, float] = {start: 0.0}
        prev_forward: Dict[int, Optional[int]] = {start: None}
        pq_forward = [(0.0, start)]
        visited_forward: Set[int] = set()
        
        # Backward search (upward from end, on reversed graph)
        dist_backward: Dict[int, float] = {end: 0.0}
        prev_backward: Dict[int, Optional[int]] = {end: None}
        pq_backward = [(0.0, end)]
        visited_backward: Set[int] = set()
        
        best_dist = float('inf')
        meeting_node = None
        
        while pq_forward or pq_backward:
            # Forward step
            if pq_forward:
                d, u = heapq.heappop(pq_forward)
                if u not in visited_forward and d < best_dist:
                    visited_forward.add(u)
                    
                    # Check if backward search reached this node
                    if u in dist_backward:
                        total = d + dist_backward[u]
                        if total < best_dist:
                            best_dist = total
                            meeting_node = u
                    
                    # Relax upward edges
                    for edge in self.upward_edges.get(u, []):
                        v = edge.target
                        new_dist = d + edge.weight
                        if new_dist < dist_forward.get(v, float('inf')):
                            dist_forward[v] = new_dist
                            prev_forward[v] = u
                            heapq.heappush(pq_forward, (new_dist, v))
            
            # Backward step (using downward edges in reverse = upward in reverse graph)
            if pq_backward:
                d, u = heapq.heappop(pq_backward)
                if u not in visited_backward and d < best_dist:
                    visited_backward.add(u)
                    
                    if u in dist_forward:
                        total = d + dist_forward[u]
                        if total < best_dist:
                            best_dist = total
                            meeting_node = u
                    
                    # In backward search, go upward = follow edges x -> u where x is higher than u
                    for edge in self.backward_upward_edges.get(u, []):
                        v = edge.source
                        new_dist = d + edge.weight
                        if new_dist < dist_backward.get(v, float('inf')):
                            dist_backward[v] = new_dist
                            prev_backward[v] = u
                            heapq.heappush(pq_backward, (new_dist, v))
        
        if meeting_node is None:
            return float('inf'), []
        
        # Reconstruct path
        path = self._reconstruct_path(prev_forward, prev_backward, meeting_node)
        return best_dist, path
    
    def _reconstruct_path(self, prev_forward: Dict, prev_backward: Dict, meeting: int) -> List[int]:
        """Reconstruct the full path from forward and backward predecessors."""
        # Forward path: start -> meeting
        path_forward = []
        node = meeting
        while node is not None:
            path_forward.append(node)
            node = prev_forward.get(node)
        path_forward.reverse()
        
        # Backward path: meeting -> end
        path_backward = []
        node = prev_backward.get(meeting)
        while node is not None:
            path_backward.append(node)
            node = prev_backward.get(node)
        
        return self._unpack_path(path_forward + path_backward)
    
    def _unpack_path(self, path: List[int]) -> List[int]:
        """Replace every shortcut hop by the original nodes it bypasses."""
        if not path:
            return path
        unpacked = [path[0]]
        for u, v in zip(path, path[1:]):
            unpacked.extend(self._unpack_edge(u, v)[1:])
        return unpacked
    
    def _unpack_edge(self, u: int, v: int) -> List[int]:
        # The query always uses the lightest edge u -> v
        best = min((e for e in self.out_edges[u] if e.target == v), key=lambda e: e.weight)
        if not isinstance(best, ShortcutEdge):
            return [u, v]
        return self._unpack_edge(u, best.via) + self._unpack_edge(best.via, v)[1:]
