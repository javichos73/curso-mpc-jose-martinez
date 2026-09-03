# Interface Contract: CLI Weight Converter

## Command Signature

```bash
python -m src.cli --value <NUMBER> --from <UNIT> [--to <UNIT>] [--json]
```

## Arguments

- `--value` / `-v` (Required, `float`): Numeric weight value to convert (must be >= 0).
- `--from` / `-f` (Required, `string`): Source unit (`kg`, `lb`, `lbs`, `oz`).
- `--to` / `-t` (Optional, `string`): Target unit (`kg`, `lb`, `lbs`, `oz`). If omitted, outputs conversions to ALL supported units.
- `--json` (Optional, flag): Output formatted as JSON instead of plain text.

## Exit Codes

- `0`: Success
- `1`: Invalid input arguments (e.g. non-numeric value, negative number, unknown unit)
- `2`: System error

## Output Formats

### Standard Text Output Example

```text
5.0 kg = 11.0231 lbs
5.0 kg = 176.3739 oz
```

### JSON Output Example (`--json`)

```json
{
  "source": {
    "value": 5.0,
    "unit": "kg"
  },
  "conversions": [
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
