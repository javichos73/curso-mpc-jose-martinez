"""
Módulo conversor de unidades de peso.
Soporta kilogramos (kg), libras (lb) y onzas (oz).
"""

UNIT_ALIASES = {
    "kg": "kg",
    "kilogramo": "kg",
    "kilogramos": "kg",
    "lb": "lb",
    "lbs": "lb",
    "libra": "lb",
    "libras": "lb",
    "oz": "oz",
    "onza": "oz",
    "onzas": "oz",
}

# Factores de conversión a kilogramos (base)
TO_KG_FACTORS = {
    "kg": 1.0,
    "lb": 0.45359237,
    "oz": 0.028349523125,
}


def _normalize_unit(unit: str) -> str:
    if not isinstance(unit, str):
        raise ValueError(f"La unidad debe ser una cadena de texto, se recibió: {type(unit).__name__}")
    
    cleaned = unit.strip().lower()
    if cleaned in UNIT_ALIASES:
        return UNIT_ALIASES[cleaned]
    
    raise ValueError(f"Unidad no soportada: '{unit}'. Usar 'kg', 'lb' o 'oz'.")


def convert_weight(value: float | int | str, from_unit: str, to_unit: str) -> float:
    """
    Convierte un valor de peso de una unidad de origen a una de destino y redondea a 2 decimales.

    Args:
        value: Valor numérico a convertir (puede ser int, float o str numérico).
        from_unit: Unidad de origen ('kg', 'lb', 'oz', etc.).
        to_unit: Unidad de destino ('kg', 'lb', 'oz', etc.).

    Returns:
        float: Resultado redondeado a 2 decimales.

    Raises:
        ValueError: Si el valor no es numérico, si el peso es negativo o si las unidades no son válidas.
    """
    # Validar que sea un número válido
    try:
        numeric_value = float(value)
    except (ValueError, TypeError):
        raise ValueError(f"Entrada no numérica inválida: '{value}'")

    # Rechazar pesos negativos
    if numeric_value < 0:
        raise ValueError(f"El peso no puede ser menor a 0. Valor ingresado: {numeric_value}")

    # Normalizar unidades
    norm_from = _normalize_unit(from_unit)
    norm_to = _normalize_unit(to_unit)

    # Conversión entre la misma unidad
    if norm_from == norm_to:
        return round(numeric_value, 2)

    # Convertir valor de origen a kg (unidad base)
    value_in_kg = numeric_value * TO_KG_FACTORS[norm_from]

    # Convertir de kg a la unidad de destino
    result = value_in_kg / TO_KG_FACTORS[norm_to]

    return round(result, 2)
