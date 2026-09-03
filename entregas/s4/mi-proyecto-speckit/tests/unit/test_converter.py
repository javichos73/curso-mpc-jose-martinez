import unittest
from src.models.weight import WeightUnit, WeightMeasurement
from src.services.converter import convert_weight, convert_all

class TestWeightConverter(unittest.TestCase):
    def test_convert_kg_to_lbs(self):
        source = WeightMeasurement(1.0, WeightUnit.KG)
        res = convert_weight(source, WeightUnit.LB)
        self.assertAlmostEqual(res.converted_value, 2.20462262, places=4)
        self.assertEqual(res.formatted_value, "2.2046")

    def test_convert_oz_to_lbs(self):
        source = WeightMeasurement(16.0, WeightUnit.OZ)
        res = convert_weight(source, WeightUnit.LB)
        self.assertAlmostEqual(res.converted_value, 1.0, places=4)
        self.assertEqual(res.formatted_value, "1")

    def test_convert_lb_to_oz(self):
        source = WeightMeasurement(1.0, WeightUnit.LB)
        res = convert_weight(source, WeightUnit.OZ)
        self.assertAlmostEqual(res.converted_value, 16.0, places=4)
        self.assertEqual(res.formatted_value, "16")

    def test_convert_same_unit(self):
        source = WeightMeasurement(5.0, WeightUnit.KG)
        res = convert_weight(source, WeightUnit.KG)
        self.assertEqual(res.converted_value, 5.0)

    def test_convert_all(self):
        source = WeightMeasurement(5.0, WeightUnit.KG)
        results = convert_all(source)
        self.assertIn(WeightUnit.KG, results)
        self.assertIn(WeightUnit.LB, results)
        self.assertIn(WeightUnit.OZ, results)
        self.assertEqual(results[WeightUnit.KG].converted_value, 5.0)
        self.assertAlmostEqual(results[WeightUnit.LB].converted_value, 11.0231, places=3)

if __name__ == '__main__':
    unittest.main()
