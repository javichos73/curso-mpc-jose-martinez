"""Pruebas unitarias para el validador de contraseñas y correos electrónicos."""

import pytest
from vibe_coding.validator import PasswordValidator, EmailValidator


def test_password_length():
    validator = PasswordValidator(min_length=8, max_length=20)
    
    # Demasiado corta
    res_short = validator.validate("Short1!")
    assert not res_short.is_valid
    assert any(not req.passed and "Longitud" in req.name for req in res_short.requirements)

    # Longitud válida
    res_ok = validator.validate("ValidPass1!")
    assert res_ok.is_valid


def test_character_requirements():
    validator = PasswordValidator(min_length=8)
    
    # Sin mayúscula
    res = validator.validate("lowercase1!")
    assert not res.is_valid
    assert any(req.name == "Incluye mayúsculas" and not req.passed for req in res.requirements)

    # Sin minúscula
    res = validator.validate("UPPERCASE1!")
    assert not res.is_valid
    assert any(req.name == "Incluye minúsculas" and not req.passed for req in res.requirements)

    # Sin número
    res = validator.validate("NoDigitsHere!")
    assert not res.is_valid
    assert any(req.name == "Incluye números" and not req.passed for req in res.requirements)

    # Sin carácter especial
    res = validator.validate("NoSpecial123")
    assert not res.is_valid
    assert any(req.name == "Incluye caracteres especiales" and not req.passed for req in res.requirements)


def test_blacklisted_password():
    validator = PasswordValidator()
    
    res = validator.validate("123456")
    assert not res.is_valid
    assert any(req.name == "No es una contraseña común" and not req.passed for req in res.requirements)

    res_custom = PasswordValidator(custom_blacklist={"miclave123"})
    res_custom_val = res_custom.validate("Miclave123!")
    assert any(req.name == "No es una contraseña común" and not req.passed for req in res_custom_val.requirements)


def test_pattern_detection():
    validator = PasswordValidator()
    
    # Repetición de caracteres "aaa"
    res = validator.validate("aaaBC123!@#")
    assert not res.is_valid
    assert any("caracteres repetidos" in sug for sug in res.suggestions)

    # Secuencia de teclado "qwerty"
    res_qwerty = validator.validate("qwertyP@ss123")
    assert not res_qwerty.is_valid


def test_entropy_and_strength():
    validator = PasswordValidator()
    
    # Contraseña débil
    res_weak = validator.validate("Password1!")
    
    # Contraseña muy fuerte
    res_strong = validator.validate("X9#kL$mP2@vN8!zQ")
    
    assert res_strong.entropy_bits > res_weak.entropy_bits
    assert res_strong.score > res_weak.score
    assert res_strong.strength_level in ("Fuerte", "Muy Fuerte")


def test_email_validation():
    validator = EmailValidator()

    # Emails válidos
    assert validator.validate("usuario@dominio.com").is_valid
    assert validator.validate("juan.perez+test@empresa.co.uk").is_valid

    # Email inválido (sin @)
    res_no_at = validator.validate("usuariodominio.com")
    assert not res_no_at.is_valid

    # Email inválido (puntos consecutivos)
    res_dots = validator.validate("usuario..nombre@dominio.com")
    assert not res_dots.is_valid

    # Dominio con sugerencia de tipeo (gmai.com -> gmail.com)
    res_typo = validator.validate("juan@gmai.com")
    assert res_typo.is_valid  # Formato sintáctico es válido pero tiene sugerencia
    assert any("gmail.com" in sug for sug in res_typo.suggestions)

    # Dominio desechable / temporal
    res_disp = validator.validate("test@tempmail.com")
    assert not res_disp.is_valid
    assert any("desechables" in err for err in res_disp.errors)


def test_password_with_email_cross_check():
    validator = PasswordValidator(min_length=8)
    
    # Contraseña que contiene la parte local del email ("jose.martinez")
    res = validator.validate("jose.martinez2026!#", email="jose.martinez@gmail.com")
    assert not res.is_valid
    assert any(req.name == "Independiente del email" and not req.passed for req in res.requirements)


def test_user_manager_batch_validation():
    from vibe_coding.validator import User, UserManager

    users = [
        User("maria@example.com", "X9#kL$mP2@vN8!zQ"),
        User("carlos@example.com", "W8!mK#nQ3@xP9$zR"),
    ]
    
    manager = UserManager(users=users)
    batch_res = manager.validate_all()

    assert batch_res.total_users == 2
    assert batch_res.valid_users_count == 2
    assert batch_res.invalid_users_count == 0
    assert len(batch_res.global_warnings) == 0




def test_user_manager_duplicate_detection():
    from vibe_coding.validator import User, UserManager

    # Email duplicado y contraseña compartida
    users = [
        User("ana@example.com", "SamePassword123!"),
        User("ana@example.com", "SamePassword123!"),
        User("luis@example.com", "SamePassword123!"),
    ]

    manager = UserManager(users=users)
    batch_res = manager.validate_all()

    assert batch_res.total_users == 3
    assert batch_res.valid_users_count == 0
    assert batch_res.invalid_users_count == 3
    assert len(batch_res.global_warnings) == 2
    assert any("duplicados" in w for w in batch_res.global_warnings)
    assert any("repetidas" in w for w in batch_res.global_warnings)


def test_admin_user_optional_password():
    from vibe_coding.validator import User, UserManager

    # Usuario administrador sin contraseña y usuario regular sin contraseña
    admin = User(email="admin@empresa.com", password="", is_admin=True)
    regular = User(email="empleado@empresa.com", password="", is_admin=False)

    manager = UserManager(users=[admin, regular])
    batch_res = manager.validate_all()

    # El admin debe ser válido sin contraseña, el usuario común debe fallar por contraseña vacía/corta
    admin_result = batch_res.user_results[0]
    regular_result = batch_res.user_results[1]

    assert admin_result[1].is_valid  # email_res
    assert admin_result[2].is_valid  # pwd_res (exento)
    assert "Exento" in admin_result[2].strength_level

    assert regular_result[1].is_valid  # email_res
    assert not regular_result[2].is_valid  # pwd_res (inválido por no tener contraseña)


