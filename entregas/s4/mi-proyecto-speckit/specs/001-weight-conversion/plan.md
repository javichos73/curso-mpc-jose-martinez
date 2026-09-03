# Implementation Plan: Weight Conversion (Kilograms, Pounds, Ounces)

**Branch**: `001-weight-conversion` | **Date**: 2026-09-02 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/001-weight-conversion/spec.md`

## Summary

Implement a lightweight, standalone Python library and CLI tool to perform bidirectional conversion between Kilograms (`kg`), Pounds (`lbs`), and Ounces (`oz`). The implementation uses a canonical unit conversion pattern (converting through Kilograms) to maintain mathematical consistency, exact factor ratios, standard decimal precision formatting, and input validation for non-negative values.

## Technical Context

**Language/Version**: Python 3.10+
**Primary Dependencies**: Standard Library (`argparse`, `dataclasses`, `enum`, `json`, `math`, `unittest`)
**Storage**: N/A (In-memory calculation)
**Testing**: Standard Library `unittest` or `pytest`
**Target Platform**: Cross-platform (CLI / Python module)
**Project Type**: Library / CLI Tool
**Performance Goals**: Instant response (< 10ms per conversion)
**Constraints**: Zero external dependencies; precision exact to 4 decimal places formatted
**Scale/Scope**: Pure weight conversion domain library with CLI wrapper

## Constitution Check

*GATE: Passed*
- **Library-First**: Core logic decoupled into `src/lib/converter.py` and models.
- **CLI Interface**: Standard input/output protocol via `src/cli.py` with text and JSON support.
- **Test-First & Integration Testing**: Unit and contract tests defined prior to code construction.

## Project Structure

### Documentation (this feature)

```text
specs/001-weight-conversion/
├── plan.md              # Implementation Plan
├── research.md          # Phase 0 research findings
├── data-model.md        # Data models and domain entities
├── quickstart.md        # Quickstart validation guide
└── contracts/
    └── cli-contract.md  # CLI contract specification
```

### Source Code (repository root)

```text
src/
├── models/
│   └── weight.py        # WeightUnit, WeightMeasurement, ConversionResult
├── services/
│   └── converter.py     # Core conversion logic and mathematical formulas
└── cli.py               # Argument parsing and user output interface

tests/
├── unit/
│   ├── test_models.py
│   └── test_converter.py
└── contract/
    └── test_cli.py
```

**Structure Decision**: Standard single project layout with `src/` modularization (models, services/logic, cli) and unit/contract test isolation in `tests/`.

## Complexity Tracking

No constitution violations present.
