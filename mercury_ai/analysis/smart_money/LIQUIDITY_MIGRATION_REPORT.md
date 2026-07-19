# Liquidity Engine Migration Report

## Overview
As part of the Liquidity Engine - Institutional Validation Layer sprint, the Equal High detection pipeline has been refactored to introduce a dedicated validation layer.

## Changes
- The `analyze()` pipeline in `LiquidityEngine` has been updated to explicitly call `validate_equal_high_groups()` after building groups and before calculating metrics.
- Validation rules for Equal High groups have been centralized within `validate_equal_high_groups()`.
- Internal debugging for validation rejections has been added to `LiquidityEngine`.
- A `generate_validation_report()` method has been added to `LiquidityEngine`.
