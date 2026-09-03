## Objetivo
Convertir valores de peso entre kilogramos, libras y onzas para permitir conversiones entre unidades.

## Criterios de aceptación
- [ ] Convierte correctamente de kilogramos a libras y viceversa.
- [ ] Convierte correctamente de onzas a kilogramos y viceversa.
- [ ] Convierte correctamente de libras a onzas y viceversa.
- [ ] Redondea el resultado final a 2 decimales.
- [ ] Rechaza valores de peso menores a 0 (no existen pesos negativos).

## Casos borde
- Entrada con texto no numérico  → debe retornar un error claro o lanzar excepción manejada sin que colapse el programa.
- Conversión entre la misma unidad  → debe devolver exactamente el mismo valor ingresado.
- Ingreso del valor cero 0 → debe retornar 0 en la unidad de destino sin errores.