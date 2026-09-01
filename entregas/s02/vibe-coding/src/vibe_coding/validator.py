"""Módulo de validación de contraseñas y correos electrónicos con análisis de fortaleza, entropía y patrones."""

from dataclasses import dataclass, field
import math
import re
from typing import List, Optional, Set, Tuple

# Lista común de contraseñas comprometidas/frecuentes
COMMON_PASSWORDS_BLACKLIST: Set[str] = {
    "123456", "password", "123456789", "12345678", "12345", "1234567", "1234",
    "qwerty", "111111", "1234567890", "123123", "abc123", "password1", "admin",
    "iloveyou", "secret", "welcome", "monkey", "dragon", "master", "letmein",
    "contrasena", "contraseña", "clave123", "admin123", "cambiar", "hola123"
}

# Dominios desechables o temporales comunes
DISPOSABLE_EMAIL_DOMAINS: Set[str] = {
    "tempmail.com", "mailinator.com", "10minutemail.com", "dispostable.com",
    "yopmail.com", "guerrillamail.com", "trashmail.com", "sharklasers.com",
    "getnada.com", "temp-mail.org"
}

# Errores comunes de tipeo en dominios populares
COMMON_DOMAIN_TYPOS = {
    "gmai.com": "gmail.com",
    "gamil.com": "gmail.com",
    "gmial.com": "gmail.com",
    "hotmai.com": "hotmail.com",
    "hotmial.com": "hotmail.com",
    "outlok.com": "outlook.com",
    "yaho.com": "yahoo.com",
    "yahou.com": "yahoo.com"
}

# Patrones de teclado comunes (QWERTY y numérico)
KEYBOARD_PATTERNS = [
    "qwertyuiop", "asdfghjkl", "zxcvbnm",
    "1234567890", "0987654321"
]

SPECIAL_CHARACTERS = set("!@#$%^&*()_+-=[]{}|;:'\",.<>/?\\~`")

# Regex estándar para formato RFC 5322 simplificado
EMAIL_REGEX = re.compile(
    r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)+$"
)


@dataclass
class ValidationRequirement:
    """Representa el estado de una regla de validación."""
    name: str
    passed: bool
    message: str


@dataclass
class ValidationResult:
    """Resultado completo de la evaluación de una contraseña."""
    is_valid: bool
    score: int  # 0 a 100
    strength_level: str  # Muy Débil, Débil, Moderada, Fuerte, Muy Fuerte
    entropy_bits: float
    requirements: List[ValidationRequirement] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)


@dataclass
class EmailValidationResult:
    """Resultado de la validación del correo electrónico."""
    is_valid: bool
    email: str
    local_part: str = ""
    domain: str = ""
    errors: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)


class EmailValidator:
    """Validador de sintaxis y formato de correo electrónico."""

    def __init__(
        self,
        check_disposable: bool = True,
        disposable_domains: Optional[Set[str]] = None
    ):
        self.check_disposable = check_disposable
        self.disposable_domains = set(DISPOSABLE_EMAIL_DOMAINS)
        if disposable_domains:
            self.disposable_domains.update(d.lower() for d in disposable_domains)

    def validate(self, email: str) -> EmailValidationResult:
        """Valida el formato, longitud, caracteres y dominio de un correo electrónico."""
        email = email.strip()
        errors = []
        suggestions = []

        if not email:
            return EmailValidationResult(
                is_valid=False,
                email=email,
                errors=["El correo electrónico no puede estar vacío."]
            )

        # 1. Longitud total (RFC 5321 max 254 chars)
        if len(email) > 254:
            errors.append("El correo excede la longitud máxima permitida de 254 caracteres.")

        # 2. Presencia de símbolo @
        if "@" not in email:
            errors.append("El correo debe contener un símbolo '@'.")
            return EmailValidationResult(is_valid=False, email=email, errors=errors)

        parts = email.split("@")
        if len(parts) != 2:
            errors.append("El correo solo debe contener un único símbolo '@'.")
            return EmailValidationResult(is_valid=False, email=email, errors=errors)

        local_part, domain = parts[0], parts[1]

        # 3. Validar local_part (usuario)
        if not local_part:
            errors.append("Falta el nombre de usuario antes del '@'.")
        elif len(local_part) > 64:
            errors.append("El nombre de usuario (antes del '@') no debe superar 64 caracteres.")
        elif local_part.startswith(".") or local_part.endswith("."):
            errors.append("El nombre de usuario no debe empezar ni terminar con punto ('.').")
        elif ".." in local_part:
            errors.append("El nombre de usuario no debe contener puntos consecutivos ('..').")

        # 4. Validar domain (dominio)
        if not domain:
            errors.append("Falta el dominio después del '@'.")
        else:
            if "." not in domain:
                errors.append("El dominio debe contener al menos una extensión (ej. '.com').")
            elif domain.startswith(".") or domain.endswith("."):
                errors.append("El dominio no debe empezar ni terminar con punto ('.').")
            elif ".." in domain:
                errors.append("El dominio no debe contener puntos consecutivos ('..').")
            else:
                tld = domain.split(".")[-1]
                if len(tld) < 2:
                    errors.append("La extensión del dominio (TLD) debe tener al menos 2 caracteres.")

        # 5. Validación con Regex estándar RFC 5322
        if not errors and not EMAIL_REGEX.match(email):
            errors.append("Formato de correo electrónico no válido según estándar RFC 5322.")

        # 6. Detección de errores comunes de tipeo en el dominio
        domain_lower = domain.lower()
        if domain_lower in COMMON_DOMAIN_TYPOS:
            suggested_domain = COMMON_DOMAIN_TYPOS[domain_lower]
            suggestions.append(f"¿Quisiste decir '{local_part}@{suggested_domain}'?")

        # 7. Verificación de dominios desechables
        if self.check_disposable and domain_lower in self.disposable_domains:
            errors.append("No se permiten correos de dominios temporales o desechables.")

        is_valid = len(errors) == 0

        return EmailValidationResult(
            is_valid=is_valid,
            email=email,
            local_part=local_part,
            domain=domain,
            errors=errors,
            suggestions=suggestions
        )


@dataclass
class User:
    """Representa a un usuario con su correo electrónico, contraseña y rol (administrador opcional)."""
    email: str
    password: str = ""
    is_admin: bool = False


@dataclass
class BatchUserValidationResult:
    """Resultado del procesamiento y validación de una lista de usuarios."""
    total_users: int
    valid_users_count: int
    invalid_users_count: int
    user_results: List[Tuple[User, EmailValidationResult, ValidationResult]] = field(default_factory=list)
    global_warnings: List[str] = field(default_factory=list)


class UserManager:
    """Gestor de una lista de usuarios con validaciones individuales y grupales."""

    def __init__(
        self,
        users: Optional[List[User]] = None,
        email_validator: Optional[EmailValidator] = None,
        password_validator: Optional["PasswordValidator"] = None
    ):
        self.users: List[User] = users if users is not None else []
        self.email_validator = email_validator or EmailValidator()
        self.password_validator = password_validator or PasswordValidator()

    def add_user(self, user: User) -> None:
        """Añade un nuevo usuario a la lista."""
        self.users.append(user)

    def validate_all(self) -> BatchUserValidationResult:
        """Valida a todos los usuarios de la lista individualmente y realiza comprobaciones cruzadas.
        
        Si el usuario es administrador (is_admin=True), la validación de contraseña es opcional.
        Si la contraseña está vacía para un administrador, se considerará válida con un aviso.
        """
        user_results = []
        global_warnings = []
        
        email_counts: dict[str, int] = {}
        password_counts: dict[str, int] = {}

        for user in self.users:
            email_normalized = user.email.strip().lower()
            email_counts[email_normalized] = email_counts.get(email_normalized, 0) + 1
            if user.password:
                password_counts[user.password] = password_counts.get(user.password, 0) + 1

        duplicate_emails = [email for email, count in email_counts.items() if count > 1]
        if duplicate_emails:
            global_warnings.append(f"Se detectaron correos electrónicos duplicados: {', '.join(duplicate_emails)}")

        duplicate_passwords_count = sum(1 for pwd, count in password_counts.items() if count > 1)
        if duplicate_passwords_count > 0:
            global_warnings.append(f"ADVERTENCIA DE SEGURIDAD: {duplicate_passwords_count} contraseña(s) están compartidas/repetidas entre múltiples usuarios.")

        valid_count = 0

        for user in self.users:
            email_res = self.email_validator.validate(user.email)

            if user.is_admin and not user.password:
                # La contraseña es opcional para administradores
                pwd_res = ValidationResult(
                    is_valid=True,
                    score=100,
                    strength_level="Administrador Sin Contraseña (Exento)",
                    entropy_bits=0.0,
                    requirements=[
                        ValidationRequirement(
                            name="Validación de Contraseña",
                            passed=True,
                            message="Contraseña opcional para usuario Administrador"
                        )
                    ],
                    suggestions=["Considera asignar una contraseña segura de todas formas para la cuenta de administrador."]
                )
            else:
                pwd_res = self.password_validator.validate(user.password, email=user.email)

            email_norm = user.email.strip().lower()
            if email_counts.get(email_norm, 0) > 1:
                email_res.is_valid = False
                email_res.errors.append("El correo electrónico está duplicado en la lista de usuarios.")

            if user.password and password_counts.get(user.password, 0) > 1:
                pwd_res.is_valid = False
                dup_req = ValidationRequirement(
                    name="Contraseña única entre usuarios",
                    passed=False,
                    message="La contraseña se repite en otro usuario de la lista"
                )
                pwd_res.requirements.append(dup_req)
                pwd_res.suggestions.append("Cambia la contraseña. Reutilizar contraseñas entre distintos usuarios aumenta el riesgo de seguridad.")

            is_user_valid = email_res.is_valid and pwd_res.is_valid
            if is_user_valid:
                valid_count += 1

            user_results.append((user, email_res, pwd_res))

        invalid_count = len(self.users) - valid_count

        return BatchUserValidationResult(
            total_users=len(self.users),
            valid_users_count=valid_count,
            invalid_users_count=invalid_count,
            user_results=user_results,
            global_warnings=global_warnings
        )


class PasswordValidator:
    """Validador de contraseñas con configuración personalizada de reglas de seguridad."""

    def __init__(
        self,
        min_length: int = 12,
        max_length: int = 128,
        require_uppercase: bool = True,
        require_lowercase: bool = True,
        require_digits: bool = True,
        require_special: bool = True,
        check_patterns: bool = True,
        check_blacklist: bool = True,
        custom_blacklist: Optional[Set[str]] = None
    ):
        self.min_length = min_length
        self.max_length = max_length
        self.require_uppercase = require_uppercase
        self.require_lowercase = require_lowercase
        self.require_digits = require_digits
        self.require_special = require_special
        self.check_patterns = check_patterns
        self.check_blacklist = check_blacklist
        
        self.blacklist = set(COMMON_PASSWORDS_BLACKLIST)
        if custom_blacklist:
            self.blacklist.update(s.lower() for s in custom_blacklist)

    def calculate_entropy(self, password: str) -> float:
        """Calcula la entropía aproximada de la contraseña en bits.
        
        Formula: E = L * log2(R)
        donde L = longitud de la contraseña, R = tamaño del conjunto de caracteres usados.
        """
        if not password:
            return 0.0

        pool_size = 0
        has_lower = any(c.islower() for c in password)
        has_upper = any(c.isupper() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in SPECIAL_CHARACTERS for c in password)
        has_other = any(
            not (c.islower() or c.isupper() or c.isdigit() or c in SPECIAL_CHARACTERS)
            for c in password
        )

        if has_lower:
            pool_size += 26
        if has_upper:
            pool_size += 26
        if has_digit:
            pool_size += 10
        if has_special:
            pool_size += len(SPECIAL_CHARACTERS)
        if has_other:
            pool_size += 30

        if pool_size == 0:
            return 0.0

        return len(password) * math.log2(pool_size)

    def _detect_pattern_issues(self, password: str) -> List[str]:
        """Detecta patrones débiles como repeticiones o secuencias del teclado."""
        issues = []
        lowered = password.lower()

        # Caracteres repetidos 3 o más veces consecutivas (ej. "aaa", "111")
        if re.search(r"(.)\1{2,}", lowered):
            issues.append("Contiene caracteres repetidos consecutivamente 3 o más veces.")

        # Secuencias de teclado
        for pattern in KEYBOARD_PATTERNS:
            for i in range(len(pattern) - 2):
                sub = pattern[i:i+3]
                if sub in lowered:
                    issues.append(f"Contiene secuencia común de teclado o números: '{sub}'")
                    break

        return issues

    def validate(self, password: str, email: Optional[str] = None) -> ValidationResult:
        """Valida la contraseña evaluando todas las reglas y calculando su puntuación."""
        requirements: List[ValidationRequirement] = []
        suggestions: List[str] = []

        # 1. Longitud
        len_passed = self.min_length <= len(password) <= self.max_length
        requirements.append(
            ValidationRequirement(
                name="Longitud adecuada",
                passed=len_passed,
                message=f"Debe tener entre {self.min_length} y {self.max_length} caracteres (actual: {len(password)})"
            )
        )
        if not len_passed and len(password) < self.min_length:
            suggestions.append(f"Aumenta la longitud a al menos {self.min_length} caracteres.")

        # 2. Mayúsculas
        if self.require_uppercase:
            has_upper = any(c.isupper() for c in password)
            requirements.append(
                ValidationRequirement(
                    name="Incluye mayúsculas",
                    passed=has_upper,
                    message="Debe contener al menos una letra mayúscula"
                )
            )
            if not has_upper:
                suggestions.append("Añade letras mayúsculas (A-Z).")

        # 3. Minúsculas
        if self.require_lowercase:
            has_lower = any(c.islower() for c in password)
            requirements.append(
                ValidationRequirement(
                    name="Incluye minúsculas",
                    passed=has_lower,
                    message="Debe contener al menos una letra minúscula"
                )
            )
            if not has_lower:
                suggestions.append("Añade letras minúsculas (a-z).")

        # 4. Números
        if self.require_digits:
            has_digit = any(c.isdigit() for c in password)
            requirements.append(
                ValidationRequirement(
                    name="Incluye números",
                    passed=has_digit,
                    message="Debe contener al menos un número (0-9)"
                )
            )
            if not has_digit:
                suggestions.append("Añade números (0-9).")

        # 5. Caracteres especiales
        if self.require_special:
            has_special = any(c in SPECIAL_CHARACTERS for c in password)
            requirements.append(
                ValidationRequirement(
                    name="Incluye caracteres especiales",
                    passed=has_special,
                    message="Debe contener al menos un carácter especial (ej. !@#$%^&*)"
                )
            )
            if not has_special:
                suggestions.append("Añade caracteres especiales (ej. !@#$%).")

        # 6. Lista negra / contraseñas comunes
        if self.check_blacklist:
            lowered = password.lower()
            # Coincidencia exacta o contención de palabras reservadas/comunes
            is_blacklisted = (
                lowered in self.blacklist or
                any(b in lowered for b in self.blacklist if len(b) >= 4)
            )
            requirements.append(
                ValidationRequirement(
                    name="No es una contraseña común",
                    passed=not is_blacklisted,
                    message="No debe coincidir ni contener palabras de la lista negra de contraseñas vulnerables"
                )
            )
            if is_blacklisted:
                suggestions.append("Esta contraseña es muy común o contiene palabras de fácil deducción. Elige una combinación única.")

        # 7. Detección de patrones
        if self.check_patterns:
            pattern_issues = self._detect_pattern_issues(password)
            no_patterns = len(pattern_issues) == 0
            requirements.append(
                ValidationRequirement(
                    name="Sin patrones ni secuencias predecibles",
                    passed=no_patterns,
                    message="Evita repeticiones continuas o secuencias como '123' o 'qwerty'"
                )
            )
            if not no_patterns:
                suggestions.extend(pattern_issues)

        # 8. Verificación de independencia con respecto al email (si se proporcionó)
        if email:
            email_val = EmailValidator().validate(email)
            if email_val.is_valid and email_val.local_part:
                user_part = email_val.local_part.lower()
                contains_email_user = len(user_part) >= 3 and user_part in password.lower()
                requirements.append(
                    ValidationRequirement(
                        name="Independiente del email",
                        passed=not contains_email_user,
                        message="La contraseña no debe contener el nombre de usuario de tu email"
                    )
                )
                if contains_email_user:
                    suggestions.append("No incluyas tu nombre de usuario del correo en la contraseña por seguridad.")

        # Determinar validez global
        is_valid = all(req.passed for req in requirements)

        # Cálculo de entropía
        entropy = self.calculate_entropy(password)

        # Cálculo de puntuación (0 - 100)
        passed_count = sum(1 for req in requirements if req.passed)
        total_reqs = len(requirements)
        req_score = (passed_count / total_reqs) * 50 if total_reqs > 0 else 0

        # Puntuación por entropía (máximo 50 puntos)
        # 60 bits de entropía = 50 puntos (excelente)
        entropy_score = min(50.0, (entropy / 60.0) * 50.0)

        total_score = int(req_score + entropy_score)
        total_score = max(0, min(100, total_score))

        # Determinar nivel de fortaleza
        if total_score < 30:
            strength_level = "Muy Débil"
        elif total_score < 50:
            strength_level = "Débil"
        elif total_score < 70:
            strength_level = "Moderada"
        elif total_score < 85:
            strength_level = "Fuerte"
        else:
            strength_level = "Muy Fuerte"

        return ValidationResult(
            is_valid=is_valid,
            score=total_score,
            strength_level=strength_level,
            entropy_bits=round(entropy, 2),
            requirements=requirements,
            suggestions=suggestions
        )
