"""Paquete principal de vibe_coding para la validación de contraseñas y correos electrónicos."""

from vibe_coding.validator import (
    PasswordValidator,
    ValidationResult,
    ValidationRequirement,
    EmailValidator,
    EmailValidationResult,
    User,
    UserManager,
    BatchUserValidationResult
)
from vibe_coding.cli import main

__all__ = [
    "PasswordValidator",
    "ValidationResult",
    "ValidationRequirement",
    "EmailValidator",
    "EmailValidationResult",
    "User",
    "UserManager",
    "BatchUserValidationResult",
    "main"
]

