# Tasks: Weight Conversion (Kilograms, Pounds, Ounces)

**Feature Branch**: `001-weight-conversion`
**Feature Directory**: `specs/001-weight-conversion`
**Spec**: [spec.md](spec.md)
**Plan**: [plan.md](plan.md)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Initial repository layout and basic module setup.

- [x] T001 Create project directories (`src/models/`, `src/services/`, `tests/unit/`, `tests/contract/`) per implementation plan
- [x] T002 Initialize `src/__init__.py` and root module files
- [x] T003 [P] Setup basic test runner configuration for `unittest`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core entity models and domain exception primitives that MUST be completed before story implementations.

- [x] T004 Create `WeightUnit` enum in `src/models/weight.py` representing `KG`, `LB`, and `OZ`
- [x] T005 Create `WeightMeasurement` data class with value and unit validation in `src/models/weight.py`
- [x] T006 Create `ConversionResult` data class in `src/models/weight.py`

**Checkpoint**: Core data models ready - domain service and CLI story implementation can now begin.

---

## Phase 3: User Story 1 - Direct Unit Weight Conversion (Priority: P1) 🎯 MVP

**Goal**: Enable direct conversions between any pair of supported units (Kilograms, Pounds, Ounces).

**Independent Test**: Convert 1 kg to lbs (expect 2.2046 lbs), 16 oz to lbs (expect 1 lb), 1 lb to oz (expect 16 oz).

### Tests for User Story 1

- [x] T007 [P] [US1] Unit test for conversion formulas in `tests/unit/test_converter.py`
- [x] T008 [P] [US1] Unit test for weight data models and unit validation in `tests/unit/test_models.py`

### Implementation for User Story 1

- [x] T009 [US1] Implement core conversion calculation logic in `src/services/converter.py` using Kilogram as intermediate canonical unit
- [x] T010 [US1] Implement single target unit conversion helper `convert_weight` in `src/services/converter.py`

**Checkpoint**: Direct unit-to-unit weight conversion logic complete and testable independently.

---

## Phase 4: User Story 2 - Instant Multi-Unit Overview (Priority: P2)

**Goal**: Provide simultaneous conversions to all supported units from a single input value.

**Independent Test**: Enter 5 kg and verify outputs for all supported units (`kg`, `lbs`, `oz`).

### Tests for User Story 2

- [x] T011 [P] [US2] Unit test for multi-unit overview conversion in `tests/unit/test_converter.py`

### Implementation for User Story 2

- [x] T012 [US2] Implement `convert_all` method in `src/services/converter.py` returning all unit equivalents
- [x] T013 [US2] Implement CLI command parser in `src/cli.py` supporting `--value`, `--from`, `--to`, and `--json` flags per contract spec `specs/001-weight-conversion/contracts/cli-contract.md`
- [x] T014 [US2] Add JSON formatting helper for multi-unit conversion output in `src/cli.py`

**Checkpoint**: Multi-unit overview via programmatic API and CLI complete.

---

## Phase 5: User Story 3 - Input Validation and Edge Handling (Priority: P3)

**Goal**: Validate user input and display user-friendly error messages for invalid values.

**Independent Test**: Provide non-numeric input or negative value `-5` and confirm error message on stderr with exit code 1.

### Tests for User Story 3

- [x] T015 [P] [US3] Contract test for CLI argument parsing and error exit codes in `tests/contract/test_cli.py`

### Implementation for User Story 3

- [x] T016 [US3] Add validation checks for negative numbers and NaN/infinity in `src/models/weight.py`
- [x] T017 [US3] Add error handling and user-friendly error message printing in `src/cli.py`

**Checkpoint**: System gracefully handles invalid inputs and edge cases.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Verification and final validation.

- [x] T018 Execute full test suite via `python -m unittest discover tests`
- [x] T019 Run quickstart validation scenarios defined in `specs/001-weight-conversion/quickstart.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Can start immediately.
- **Foundational (Phase 2)**: Depends on Setup (Phase 1).
- **User Story 1 (Phase 3)**: Depends on Foundational (Phase 2).
- **User Story 2 (Phase 4)**: Depends on User Story 1 (Phase 3).
- **User Story 3 (Phase 5)**: Depends on User Story 2 (Phase 4).
- **Polish (Phase 6)**: Depends on all User Stories being complete.

---

## Implementation Strategy

### MVP Scope (User Story 1 Only)
1. Complete Phase 1 (Setup)
2. Complete Phase 2 (Foundational)
3. Complete Phase 3 (User Story 1)
4. Validate MVP functionality using unit tests in `tests/unit/test_converter.py`
