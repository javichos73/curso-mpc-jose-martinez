import pytest
from weight_converter import convert_weight


def test_kg_to_lb():
    # 1 kg = ~2.20462 lb -> 2.20
    assert convert_weight(1, "kg", "lb") == 2.2
    # 5 kg = ~11.0231 lb -> 11.02
    assert convert_weight(5, "kg", "lb") == 11.02


def test_lb_to_kg():
    # 1 lb = ~0.45359 kg -> 0.45
    assert convert_weight(1, "lb", "kg") == 0.45
    # 10 lb = ~4.5359 kg -> 4.54
    assert convert_weight(10, "lb", "kg") == 4.54


def test_oz_to_kg():
    # 1 oz = ~0.02835 kg -> 0.03
    assert convert_weight(1, "oz", "kg") == 0.03
    # 100 oz = ~2.83495 kg -> 2.83
    assert convert_weight(100, "oz", "kg") == 2.83


def test_kg_to_oz():
    # 1 kg = ~35.27396 oz -> 35.27
    assert convert_weight(1, "kg", "oz") == 35.27


def test_lb_to_oz():
    # 1 lb = 16 oz
    assert convert_weight(1, "lb", "oz") == 16.0
    # 2.5 lb = 40 oz
    assert convert_weight(2.5, "lb", "oz") == 40.0


def test_oz_to_lb():
    # 16 oz = 1 lb
    assert convert_weight(16, "oz", "lb") == 1.0
    # 8 oz = 0.5 lb
    assert convert_weight(8, "oz", "lb") == 0.5


def test_rounding():
    # 12.3456 kg to lb -> 12.3456 * 2.20462262 = 27.2173... -> 27.22
    assert convert_weight(12.3456, "kg", "lb") == 27.22


def test_reject_negative_values():
    with pytest.raises(ValueError, match="menor a 0|negativo"):
        convert_weight(-1, "kg", "lb")

    with pytest.raises(ValueError, match="menor a 0|negativo"):
        convert_weight(-0.01, "lb", "oz")


def test_non_numeric_input():
    with pytest.raises(ValueError, match="inválida"):
        convert_weight("abc", "kg", "lb")

    with pytest.raises(ValueError, match="inválida"):
        convert_weight(None, "kg", "lb")


def test_same_unit_conversion():
    assert convert_weight(5, "kg", "kg") == 5.0
    assert convert_weight(12.345, "lb", "lb") == 12.35
    assert convert_weight(0, "oz", "oz") == 0.0


def test_zero_value():
    assert convert_weight(0, "kg", "lb") == 0.0
    assert convert_weight(0, "oz", "kg") == 0.0
    assert convert_weight(0, "lb", "oz") == 0.0


def test_unit_aliases():
    assert convert_weight(1, "kilogramos", "libras") == 2.2
    assert convert_weight(16, "onza", "libra") == 1.0
