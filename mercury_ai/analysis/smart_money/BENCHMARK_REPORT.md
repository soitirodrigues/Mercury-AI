# LiquidityEngine Benchmark Report

## Overview
This benchmark evaluates the performance of the `LiquidityEngine.analyze()` pipeline, specifically focusing on the new Bron-Kerbosch maximal clique grouping logic, across varying input sizes.

## Performance Results

| Number of Swings | Execution Time (s) | Peak Memory (MB) |
| :--- | :--- | :--- |
| 100 | 0.1570 | 0.2400 |
| 200 | 0.4838 | 0.7308 |
| 500 | 9.1086 | 3.4146 |
| 1000 | 49.2972 | 11.7023 |

## Big-O Estimation
- **Time Complexity:** The execution time grows super-linearly, consistent with the exponential worst-case complexity of the Bron-Kerbosch algorithm ($O(3^{N/3})$). Based on these measurements, the current implementation is not suitable for $N > 1000$ in real-time scenarios.
- **Memory Complexity:** Memory usage grows roughly $O(N^2)$, dominated by the adjacency matrix used to represent pairwise swing compatibility.

## Optimization Opportunities
- **Graph Pruning:** Implement pre-clustering filtering to reduce $N$ before the adjacency matrix construction and clique identification.
- **Adjacency Representation:** Use sparse matrix representations (e.g., `scipy.sparse`) for the compatibility graph to improve memory usage from $O(N^2)$ to $O(E)$ (where $E$ is the number of edges).
- **Bron-Kerbosch Heuristics:** Further refine pivot selection or implement BitSet-based Bron-Kerbosch to significantly accelerate clique identification for larger graphs.
- **Incremental Analysis:** If market data arrives sequentially, implement incremental clique updates rather than re-computing the entire graph.
