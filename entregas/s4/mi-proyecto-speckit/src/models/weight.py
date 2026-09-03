from dataclasses import dataclass
from enum import Enum
import math

class WeightUnit(Enum):
    KG = "kg"
    LB = "lbs"
    OZ = "oz"

    @classmethod
    def from_string(cls, unit_str: str) -> "WeightUnit":
        cleaned = unit_str.strip().lower()
        if cleaned in ("kg", "kilogram", "kilograms"):
            return cls.KG
        elif cleaned in ("lb", "lbs", "pound", "pounds"):
            return cls.LB
        elif cleaned in ("oz", "ounce", "ounces"):
            return cls.OZ
        else:
            raise ValueError(f"Unsupported weight unit: '{unit_str}'. Supported units are kg, lbs, oz.")

@dataclass(frozen=True)
class WeightMeasurement:
    value: float
    unit: WeightUnit

    def __post_init__(self):
        if not isinstance(self.value, (int, float)) or math.isnan(self.value) or math.isinf(self.value):
            raise ValueError("Weight value must be a valid finite number.")
        if self.value < 0:
            raise ValueError("Weight value must be zero or positive.")

@dataclass(frozen=True)
class ConversionResult:
    source: WeightMeasurement
    target_unit: WeightUnit
    converted_value: float
    formatted_value: str
