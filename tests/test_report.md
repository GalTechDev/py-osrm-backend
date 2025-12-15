# Test Report - py-osrm-backend

**Date**: 2025-12-10 12:24:57

**Python**: 3.10.8

## Summary
- **Tests Run**: 10
- **Passed**: 10
- **Failures**: 0
- **Errors**: 0

**Status**: ✅ ALL TESTS PASSED

## Test Details
```
test_preprocessing (test_ch.TestContractionHierarchies) ... ok
test_query_shortest_path (test_ch.TestContractionHierarchies) ... ok
test_direct_path (test_engine.TestDijkstra) ... ok
test_no_path (test_engine.TestDijkstra) ... ok
test_shortest_path_via_intermediate (test_engine.TestDijkstra) ... ok
test_build_graph_from_osm (test_extractor.TestExtractor) ... ok
test_add_edge (test_structures.TestGraph) ... ok
test_add_node (test_structures.TestGraph) ... ok
test_haversine_distance (test_structures.TestGraph) ... ok
test_node_creation (test_structures.TestNode) ... ok

----------------------------------------------------------------------
Ran 10 tests in 0.002s

OK

```