# Data Model: Weight Conversion

## Entities

### 1. `WeightUnit` (Enum)
Represents supported mass/weight units.

- **Values**:
  - `KG` (Kilograms, symbol: `kg`)
  - `LB` (Pounds, symbol: `lbs` or `lb`)
  - `OZ` (Ounces, symbol: `oz`)

### 2. `WeightMeasurement` (Data Class / Value Object)
Represents a specific weight quantity.

- **Attributes**:
  - `value`: `float` (Must be >= 0)
  - `unit`: `WeightUnit`
- **Validation Rules**:
  - `value` cannot be negative (`value < 0` raises `ValueError`).
  - `value` must be a valid finite number (`NaN` / `Infinity` raises `ValueError`).

### 3. `ConversionResult` (Value Object / Schema)
Represents the result of converting a weight measurement to target unit(s).

- **Attributes**:
  - `source`: `WeightMeasurement`
  - `target_unit`: `WeightUnit`
  - `converted_value`: `float`
  - `formatted_value`: `str` (Rounded to 4 decimal places by default)

## Domain Methods / Operations

- `convert_weight(measurement: WeightMeasurement, target_unit: WeightUnit) -> ConversionResult`
- `convert_all(measurement: WeightMeasurement) -> Dict[WeightUnit, ConversionResult]`
