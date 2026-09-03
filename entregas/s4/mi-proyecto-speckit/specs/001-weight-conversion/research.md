# Phase 0 Research: Weight Conversion

## Overview
This research resolves implementation choices for building a lightweight weight conversion utility/library supporting Kilograms (`kg`), Pounds (`lbs`), and Ounces (`oz`).

## Technology & Environment Choices

### 1. Language & Ecosystem
- **Decision**: Python 3.10+ (Standard Library only).
- **Rationale**: Python provides clean syntax, arbitrary precision math options, standard unit test frameworks (`unittest`/`pytest`), and seamless CLI script execution without external third-party dependency overhead.
- **Alternatives Considered**: Node.js/TypeScript (adds `package.json` setup overhead), Rust (overkill for simple weight conversion utility).

### 2. Architecture & Pattern
- **Decision**: Standalone Conversion Module / Library with CLI and programmatic Python API.
- **Rationale**: Follows modular Unix/library-first design principles. The conversion logic is isolated in a pure converter module, which can be imported as a library or invoked via CLI.
- **Alternatives Considered**: Monolithic script combining CLI parsing and mathematical conversion into one file (rejected to maintain clear separation of concerns and testability).

### 3. Conversion Precision & Factor Strategy
- **Decision**: Use exact base conversion ratio in reference to Kilograms:
  - 1 kg = 2.2046226218487758 lbs
  - 1 lb = 16 oz (exact)
  - 1 kg = 35.273961949580414 oz
  Standard output rounding defaults to 4 decimal places unless exact representation is requested.
- **Rationale**: Using precise standard conversion constants ensures cross-unit consistency (e.g. converting kg -> lb -> oz matches kg -> oz).
- **Alternatives Considered**: Pre-calculated static lookup matrix for every pair (rejected in favor of intermediate canonical unit `Kilogram` conversion to simplify scaling to future units).

### 4. Input Validation & Error Handling
- **Decision**: Strict validation of numeric values; reject non-numeric inputs and values `< 0` with explicit domain exceptions (`ValueError` / custom `InvalidWeightError`).
- **Rationale**: Physical mass/weight in standard contexts cannot be negative.
- **Alternatives Considered**: Silent fallback to `0` (rejected as it hides user input errors).
