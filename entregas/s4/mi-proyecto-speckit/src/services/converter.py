from typing import Dict
from src.models.weight import WeightUnit, WeightMeasurement, ConversionResult

# Exact factors relative to Kilograms (1 kg = 2.2046226218487758 lbs, 1 lb = 16 oz)
KG_TO_LB = 2.2046226218487758
LB_TO_OZ = 16.0
KG_TO_OZ = KG_TO_LB * LB_TO_OZ

def _to_kg(measurement: WeightMeasurement) -> float:
    if measurement.unit == WeightUnit.KG:
        return measurement.value
    elif measurement.unit == WeightUnit.LB:
        return measurement.value / KG_TO_LB
    elif measurement.unit == WeightUnit.OZ:
        return measurement.value / KG_TO_OZ
    else:
        raise ValueError(f"Unsupported unit: {measurement.unit}")

def _from_kg(kg_value: float, target_unit: WeightUnit) -> float:
    if target_unit == WeightUnit.KG:
        return kg_value
    elif target_unit == WeightUnit.LB:
        return kg_value * KG_TO_LB
    elif target_unit == WeightUnit.OZ:
        return kg_value * KG_TO_OZ
    else:
        raise ValueError(f"Unsupported target unit: {target_unit}")

def format_precision(val: float, precision: int = 4) -> str:
    rounded = round(val, precision)
    if rounded == int(rounded):
        return str(int(rounded))
    formatted = f"{rounded:.{precision}f}".rstrip('0').rstrip('.')
    return formatted

def convert_weight(measurement: WeightMeasurement, target_unit: WeightUnit) -> ConversionResult:
    kg_val = _to_kg(measurement)
    target_val = _from_kg(kg_val, target_unit)
    formatted = format_precision(target_val)
    return ConversionResult(
        source=measurement,
        target_unit=target_unit,
        converted_value=target_val,
        formatted_value=formatted
    )

def convert_all(measurement: WeightMeasurement) -> Dict[WeightUnit, ConversionResult]:
    results = {}
    for unit in WeightUnit:
        results[unit] = convert_weight(measurement, unit)
    return results
