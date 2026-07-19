# Immutability Report

## Overview
The `LiquidityEngine` data structures (`EqualHighGroup`, `EqualHighMetrics`, `EqualHighScore`) have been refactored to enforce strict immutability.

## Changes
- Updated dataclasses to `frozen=True`.
- Refactored `LiquidityEngine` methods to return new object instances instead of mutating existing ones.
- Ensured no pipeline stage mutates objects received from previous stages.
- Verified immutability using standard Python object identity checks during test execution.
