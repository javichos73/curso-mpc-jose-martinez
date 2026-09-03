import unittest
import subprocess
import sys
import json

class TestCLIContract(unittest.TestCase):
    def run_cli(self, args):
        cmd = [sys.executable, "-m", "src.cli"] + args
        res = subprocess.run(cmd, capture_output=True, text=True)
        return res

    def test_single_conversion_text(self):
        res = self.run_cli(["--value", "1", "--from", "kg", "--to", "lbs"])
        self.assertEqual(res.returncode, 0)
        self.assertIn("1.0 kg = 2.2046 lbs", res.stdout.strip())

    def test_single_conversion_json(self):
        res = self.run_cli(["--value", "16", "--from", "oz", "--to", "lbs", "--json"])
        self.assertEqual(res.returncode, 0)
        data = json.loads(res.stdout)
        self.assertEqual(data["source"]["value"], 16.0)
        self.assertEqual(data["source"]["unit"], "oz")
        self.assertEqual(len(data["conversions"]), 1)
        self.assertEqual(data["conversions"][0]["unit"], "lbs")
        self.assertEqual(data["conversions"][0]["value"], 1.0)

    def test_overview_json(self):
        res = self.run_cli(["--value", "5", "--from", "kg", "--json"])
        self.assertEqual(res.returncode, 0)
        data = json.loads(res.stdout)
        self.assertEqual(len(data["conversions"]), 3)

    def test_negative_input_error(self):
        res = self.run_cli(["--value", "-5", "--from", "kg"])
        self.assertEqual(res.returncode, 1)
        self.assertIn("Error:", res.stderr)

    def test_invalid_unit_error(self):
        res = self.run_cli(["--value", "10", "--from", "invalid_unit"])
        self.assertEqual(res.returncode, 1)
        self.assertIn("Error:", res.stderr)

if __name__ == '__main__':
    unittest.main()
