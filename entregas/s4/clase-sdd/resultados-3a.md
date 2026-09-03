# Caso normal: Convertir 5 kg a libras (Resultado esperado: ~11.02 lb).

convert_weight(5, "kg", "lb")
11.02

# Caso borde de tu spec: Convertir -10 kg a libras (Resultado esperado: mensaje de error o rechazo explícito).

convert_weight(-10, "kg", "lb")
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/home/jose_martinez/proyectos/cursos/curso-mcp-jose-martinez/entregas/s4/clase-sdd/weight_converter.py", line 61, in convert_weight
    raise ValueError(f"El peso no puede ser menor a 0. Valor ingresado: {numeric_value}")
ValueError: El peso no puede ser menor a 0. Valor ingresado: -10.

# Caso no contemplado: Probar una unidad que NO pusiste en la spec, como toneladas (t) o onzas (oz).

convert_weight(10, "t", "kg")
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/home/jose_martinez/proyectos/cursos/curso-mcp-jose-martinez/entregas/s4/clase-sdd/weight_converter.py", line 64, in convert_weight
    norm_from = _normalize_unit(from_unit)
                ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/jose_martinez/proyectos/cursos/curso-mcp-jose-martinez/entregas/s4/clase-sdd/weight_converter.py", line 35, in _normalize_unit
    raise ValueError(f"Unidad no soportada: '{unit}'. Usar 'kg', 'lb' o 'oz'.")
ValueError: Unidad no soportada: 't'. Usar 'kg', 'lb' o 'oz'.