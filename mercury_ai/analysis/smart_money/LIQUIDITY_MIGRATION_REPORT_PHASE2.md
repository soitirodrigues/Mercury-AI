# Liquidity Engine Migration Report - Phase 2

## Overview
The `build_equal_high_groups()` function has been fundamentally refactored to replace the greedy clustering algorithm with a deterministic maximum compatibility algorithm (maximal clique identification using Bron-Kerbosch).

## Changes
- Replaced greedy grouping with an adjacency matrix and Bron-Kerbosch algorithm for finding maximal cliques of fully compatible swings.
- Eliminated transitive contamination: every pair in an Equal High group is guaranteed to be compatible.
- Guaranteed deterministic grouping: identical input data now produces identical cluster outputs, regardless of processing order.
- Trim groups exceeding `maximum_touches` during the clique processing stage.
- Maintained strict separation of responsibilities: grouping is decoupled from validation.
