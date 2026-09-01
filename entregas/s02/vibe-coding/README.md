# Validador de Contraseñas y Correos Electrónicos (vibe-coding)

Un validador completo y robusto escrito en Python con interfaz de línea de comandos (CLI) interactiva para evaluar la fortaleza de contraseñas y la validez de correos electrónicos.

---

## 🚀 Funcionalidades

### 🔐 Validador de Contraseñas
- **Reglas de Seguridad Configurables**: Longitud (12-128 chars), mayúsculas, minúsculas, números y caracteres especiales.
- **Cálculo de Entropía ($E = L \times \log_2(R)$)**: Medición matemática de aleatoriedad en bits.
- **Detección de Patrones**: Identificación de secuencias de teclado (`qwerty`, `12345`) y repeticiones (`aaa`).
- **Lista Negra**: Bloqueo de contraseñas vulnerables y comunes.
- **Validación Cruzada con Email**: Alerta si la contraseña contiene el nombre de usuario del correo electrónico.

### 📧 Validador de Correo Electrónico
- **Formato RFC 5322**: Verificación de sintaxis, usuario y dominio.
- **Restricciones de Longitud**: Validación de máximo 64 caracteres en el usuario y 254 caracteres en total.
- **Detección de Errores de Tipeo (Typos)**: Sugerencias automáticas para dominios populares (ej. `@gmai.com` -> `@gmail.com`).
- **Bloqueo de Dominios Temporales**: Detección de correos desechables (`tempmail.com`, `yopmail.com`, `10minutemail.com`, etc.).

---

## 🛠️ Instalación y Uso

### 1. Ejecución desde CLI

```bash
# Modo Interactivo (Menú con opciones para Email, Contraseña o Ambos)
uv run vibe-coding

# Validar sólo un Correo Electrónico
uv run vibe-coding "usuario@gmai.com"

# Validar sólo una Contraseña
uv run vibe-coding "X9#kL$mP2@vN8!zQ"

# Validar Combinación Email + Contraseña
uv run vibe-coding "usuario@empresa.com" "MiClaveSuperSegura#2026"
```

### 2. Uso como Módulo Python

```python
from vibe_coding import PasswordValidator, EmailValidator

# 1. Validar un Correo Electrónico
email_validator = EmailValidator(check_disposable=True)
email_res = email_validator.validate("juan.perez@gmai.com")

print(f"¿Email válido?: {email_res.is_valid}")
if email_res.suggestions:
    print(f"Sugerencia: {email_res.suggestions[0]}")

# 2. Validar una Contraseña (opcionalmente asociada al email)
pwd_validator = PasswordValidator(min_length=12)
pwd_res = pwd_validator.validate("JuanPerez#2026!", email="juan.perez@gmai.com")

print(f"¿Contraseña válida?: {pwd_res.is_valid}")
print(f"Fortaleza: {pwd_res.strength_level}")
print(f"Entropía: {pwd_res.entropy_bits} bits")
```

---

## 🧪 Pruebas Unitarias

Para ejecutar la suite de pruebas unitarias:

```bash
uv run pytest
```
