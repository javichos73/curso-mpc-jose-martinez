import unittest
import math
from src.models.weight import WeightUnit, WeightMeasurement

class TestWeightModels(unittest.TestCase):
    def test_unit_from_string(self):
        self.assertEqual(WeightUnit.from_string("kg"), WeightUnit.KG)
        self.assertEqual(WeightUnit.from_string("lbs"), WeightUnit.LB)
        self.assertEqual(WeightUnit.from_string("lb"), WeightUnit.LB)
        self.assertEqual(WeightUnit.from_string("oz"), WeightUnit.OZ)

    def test_invalid_unit_raises(self):
        with self.assertRaises(ValueError):
            WeightUnit.from_string("grams")

    def test_valid_measurement(self):
        wm = WeightMeasurement(10.5, WeightUnit.KG)
        self.assertEqual(wm.value, 10.5)
        self.assertEqual(wm.unit, WeightUnit.KG)

    def test_negative_weight_raises(self):
        with self.assertRaises(ValueError):
            WeightMeasurement(-1.0, WeightUnit.KG)

    def test_nan_weight_raises(self):
        with self.assertRaises(ValueError):
            WeightMeasurement(float('nan'), WeightUnit.LB)

if __name__ == '__main__':
    unittest.main()
