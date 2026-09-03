# Resultados de Pruebas — Bloque 3.B (Spec Kit)

## Pruebas Ejecutadas sobre la CLI

### 1. Caso normal: Convertir 5 kg a libras
```bash
uv run python -m src.cli --value 5 --from kg --to lb
```
**Resultado:** 5.0 kg = 11.0231 lbs

### 2. Caso borde de la spec: Valor de peso negativo (-10 kg)
```bash
uv run python -m src.cli --value -10 --from kg --to lb
```
**Resultado:** Error: Weight value must be zero or positive.

### 3. Caso no contemplado: Unidad no soportada ('t' / toneladas)
```bash
uv run python -m src.cli --value 10 --from t --to kg
```
**Resultado:** Error: Unsupported weight unit: 't'. Supported units are kg, lbs, oz.