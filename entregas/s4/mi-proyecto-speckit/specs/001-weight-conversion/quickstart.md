# Quickstart & Validation Guide: Weight Conversion

This guide describes how to run end-to-end scenarios to validate the weight conversion feature once implemented.

## Prerequisites

- Python 3.10+ installed

## Verification Scenarios

### Scenario 1: Convert 1 Kilogram to Pounds

**Command**:
```bash
python -m src.cli --value 1 --from kg --to lbs
```

**Expected Output**:
```text
1.0 kg = 2.2046 lbs
```

### Scenario 2: Convert 16 Ounces to Pounds

**Command**:
```bash
python -m src.cli --value 16 --from oz --to lbs
```

**Expected Output**:
```text
16.0 oz = 1.0 lbs
```

### Scenario 3: Overview Conversion (Multi-Unit Output)

**Command**:
```bash
python -m src.cli --value 5 --from kg --json
```

**Expected JSON Output**:
```json
{
  "source": {
    "value": 5.0,
    "unit": "kg"
  },
  "conversions": [
    {
      "unit": "kg",
      "value": 5.0
    },
    {
      "unit": "lbs",
      "value": 11.0231
    },
    {
      "unit": "oz",
      "value": 176.3739
    }
  ]
}
```

### Scenario 4: Negative Input Validation Error

**Command**:
```bash
python -m src.cli --value -5 --from kg
```

**Expected Output (Stderr, Exit Code 1)**:
```text
Error: Weight value must be zero or positive.
```
