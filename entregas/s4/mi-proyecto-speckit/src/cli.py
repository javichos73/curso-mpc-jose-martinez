import argparse
import json
import sys
from src.models.weight import WeightUnit, WeightMeasurement
from src.services.converter import convert_weight, convert_all

def main():
    parser = argparse.ArgumentParser(description="Weight Conversion Tool (Kilograms, Pounds, Ounces)")
    parser.add_argument("--value", "-v", type=float, required=True, help="Numeric weight value")
    parser.add_argument("--from", "-f", dest="from_unit", type=str, required=True, help="Source unit (kg, lbs, oz)")
    parser.add_argument("--to", "-t", dest="to_unit", type=str, default=None, help="Target unit (kg, lbs, oz)")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")

    try:
        args = parser.parse_args()
    except SystemExit as e:
        sys.exit(e.code)

    try:
        source_unit = WeightUnit.from_string(args.from_unit)
        measurement = WeightMeasurement(args.value, source_unit)

        if args.to_unit:
            target_unit = WeightUnit.from_string(args.to_unit)
            res = convert_weight(measurement, target_unit)
            results = [res]
        else:
            all_res = convert_all(measurement)
            results = list(all_res.values())

        if args.json:
            output = {
                "source": {
                    "value": measurement.value,
                    "unit": measurement.unit.value
                },
                "conversions": [
                    {
                        "unit": r.target_unit.value,
                        "value": round(r.converted_value, 4),
                        "formatted": r.formatted_value
                    } for r in results
                ]
            }
            print(json.dumps(output, indent=2))
        else:
            for r in results:
                print(f"{measurement.value} {measurement.unit.value} = {r.formatted_value} {r.target_unit.value}")

    except ValueError as err:
        print(f"Error: {err}", file=sys.stderr)
        sys.exit(1)
    except Exception as err:
        print(f"Unexpected Error: {err}", file=sys.stderr)
        sys.exit(2)

if __name__ == "__main__":
    main()
