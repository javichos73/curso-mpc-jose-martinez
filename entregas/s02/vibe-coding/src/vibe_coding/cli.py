"""Interfaz de línea de comandos (CLI) interactiva para la validación de contraseñas y correos electrónicos."""

import getpass
import sys
from typing import Optional
from vibe_coding.validator import (
    PasswordValidator,
    ValidationResult,
    EmailValidator,
    EmailValidationResult,
    User,
    UserManager,
    BatchUserValidationResult
)

# Códigos de colores ANSI para la consola
COLOR_RESET = "\033[0m"
COLOR_GREEN = "\033[92m"
COLOR_YELLOW = "\033[93m"
COLOR_RED = "\033[91m"
COLOR_CYAN = "\033[96m"
COLOR_BOLD = "\033[1m"


def get_strength_color(level: str) -> str:
    """Devuelve el código ANSI de color según el nivel de fortaleza."""
    if level in ("Fuerte", "Muy Fuerte"):
        return COLOR_GREEN
    elif level == "Moderada":
        return COLOR_YELLOW
    else:
        return COLOR_RED


def render_progress_bar(score: int, length: int = 20) -> str:
    """Genera una barra de progreso visual para la puntuación."""
    filled = int(length * (score / 100))
    bar = "█" * filled + "░" * (length - filled)
    color = COLOR_GREEN if score >= 70 else (COLOR_YELLOW if score >= 50 else COLOR_RED)
    return f"{color}[{bar}] {score}/100{COLOR_RESET}"


def print_email_result(result: EmailValidationResult) -> None:
    """Imprime el resultado del análisis del correo electrónico."""
    print("\n" + "=" * 50)
    print(f"{COLOR_BOLD}{COLOR_CYAN}ANÁLISIS DE CORREO ELECTRÓNICO{COLOR_RESET}")
    print("=" * 50)
    print(f"Email evaluado: {result.email}")
    status_str = f"{COLOR_GREEN}✓ VÁLIDO{COLOR_RESET}" if result.is_valid else f"{COLOR_RED}✗ INVÁLIDO{COLOR_RESET}"
    print(f"Estado: {status_str}")

    if result.is_valid:
        print(f"Usuario: {result.local_part}")
        print(f"Dominio: {result.domain}")

    if result.errors:
        print(f"\n{COLOR_BOLD}{COLOR_RED}Errores detectados:{COLOR_RESET}")
        for err in result.errors:
            print(f"  ✗ {err}")

    if result.suggestions:
        print(f"\n{COLOR_BOLD}{COLOR_YELLOW}Sugerencias:{COLOR_RESET}")
        for sug in result.suggestions:
            print(f"  • {sug}")

    print("=" * 50 + "\n")


def print_password_result(result: ValidationResult) -> None:
    """Imprime el resultado detallado de la validación de contraseña en pantalla."""
    color = get_strength_color(result.strength_level)

    print("\n" + "=" * 50)
    print(f"{COLOR_BOLD}{COLOR_CYAN}RESULTADO DEL ANÁLISIS DE CONTRASEÑA{COLOR_RESET}")
    print("=" * 50)

    # Estado global
    status_str = f"{COLOR_GREEN}✓ VÁLIDA{COLOR_RESET}" if result.is_valid else f"{COLOR_RED}✗ INCUMPLE REQUISITOS{COLOR_RESET}"
    print(f"Estado: {status_str}")
    print(f"Fortaleza: {color}{COLOR_BOLD}{result.strength_level}{COLOR_RESET}")
    print(f"Entropía: {result.entropy_bits} bits")
    print(f"Puntuación: {render_progress_bar(result.score)}")

    print(f"\n{COLOR_BOLD}Requisitos Evaluados:{COLOR_RESET}")
    for req in result.requirements:
        icon = f"{COLOR_GREEN}✓{COLOR_RESET}" if req.passed else f"{COLOR_RED}✗{COLOR_RESET}"
        print(f"  {icon} {req.name}: {req.message}")

    if result.suggestions:
        print(f"\n{COLOR_BOLD}{COLOR_YELLOW}Sugerencias de mejora:{COLOR_RESET}")
        for sug in result.suggestions:
            print(f"  • {sug}")

    print("=" * 50 + "\n")


def print_batch_result(batch_res: BatchUserValidationResult) -> None:
    """Imprime el resumen y análisis completo de una lista de usuarios."""
    print("\n" + "#" * 60)
    print(f"{COLOR_BOLD}{COLOR_CYAN}RESUMEN DE VALIDACIÓN DE LISTA DE USUARIOS ({batch_res.total_users} usuarios){COLOR_RESET}")
    print("#" * 60)
    print(f"Usuarios Válidos: {COLOR_GREEN}{batch_res.valid_users_count}{COLOR_RESET}")
    print(f"Usuarios Inválidos: {COLOR_RED}{batch_res.invalid_users_count}{COLOR_RESET}")

    if batch_res.global_warnings:
        print(f"\n{COLOR_BOLD}{COLOR_YELLOW}ADVERTENCIAS GLOBALES DE SEGURIDAD/DUPLICADOS:{COLOR_RESET}")
        for warn in batch_res.global_warnings:
            print(f"  ⚠️  {warn}")

    print("\n" + "-" * 60)
    for idx, (user, email_res, pwd_res) in enumerate(batch_res.user_results, 1):
        is_user_valid = email_res.is_valid and pwd_res.is_valid
        user_status = f"{COLOR_GREEN}✓ VÁLIDO{COLOR_RESET}" if is_user_valid else f"{COLOR_RED}✗ INVÁLIDO{COLOR_RESET}"
        role_tag = f" {COLOR_CYAN}[ADMIN]{COLOR_RESET}" if user.is_admin else ""
        
        print(f"\n[{idx}] Usuario: {COLOR_BOLD}{user.email}{COLOR_RESET}{role_tag} -> {user_status}")
        
        if not email_res.is_valid:
            print(f"   {COLOR_RED}Errores en Email:{COLOR_RESET}")
            for err in email_res.errors:
                print(f"     - {err}")
        
        pwd_color = get_strength_color(pwd_res.strength_level)
        print(f"   Fortaleza Contraseña: {pwd_color}{pwd_res.strength_level}{COLOR_RESET} (Puntuación: {pwd_res.score}/100)")
        
        if not pwd_res.is_valid:
            print(f"   {COLOR_RED}Errores en Contraseña:{COLOR_RESET}")
            for req in pwd_res.requirements:
                if not req.passed:
                    print(f"     - {req.name}: {req.message}")

    print("#" * 60 + "\n")


def interactive_mode(pwd_validator: PasswordValidator, email_validator: EmailValidator) -> None:
    """Ejecuta el bucle interactivo del validador."""
    print(f"{COLOR_BOLD}{COLOR_CYAN}=== Validador de Email y Contraseñas Interactivo ==={COLOR_RESET}")
    print("Opciones disponibles:")
    print("  1. Validar Correo Electrónico")
    print("  2. Validar Contraseña")
    print("  3. Validar Combinación Email + Contraseña")
    print("  4. Validar Lista de Usuarios (Soporta Administradores)")
    print("  Escribe 'salir' en cualquier momento para terminar.\n")

    while True:
        try:
            opcion = input(f"{COLOR_BOLD}Selecciona una opción (1/2/3/4): {COLOR_RESET}").strip()
            if opcion.lower() == "salir":
                print("¡Hasta luego!")
                break

            if opcion == "1":
                email = input("Ingresa el correo electrónico: ").strip()
                if email.lower() == "salir":
                    break
                result = email_validator.validate(email)
                print_email_result(result)

            elif opcion == "2":
                password = getpass.getpass(prompt="Ingresa la contraseña a evaluar: ")
                if password.strip().lower() == "salir":
                    break
                result = pwd_validator.validate(password)
                print_password_result(result)

            elif opcion == "3":
                email = input("Ingresa el correo electrónico: ").strip()
                if email.lower() == "salir":
                    break
                email_res = email_validator.validate(email)
                print_email_result(email_res)

                password = getpass.getpass(prompt="Ingresa la contraseña a evaluar (o presiona Enter si es admin): ")
                if password.strip().lower() == "salir":
                    break
                
                is_admin_in = input("¿Es usuario Administrador? (s/n): ").strip().lower()
                is_admin = is_admin_in in ("s", "si", "sí", "y", "yes")

                if is_admin and not password:
                    print(f"\n{COLOR_CYAN}Usuario marcado como Administrador sin contraseña. Exento de validación de contraseña.{COLOR_RESET}")
                else:
                    pwd_res = pwd_validator.validate(password, email=email)
                    print_password_result(pwd_res)

            elif opcion == "4":
                user_manager = UserManager(
                    email_validator=email_validator,
                    password_validator=pwd_validator
                )
                print("\nIngresa los usuarios uno a uno. Escribe 'fin' en el correo para terminar de agregar.")
                user_idx = 1
                while True:
                    email_in = input(f"\nEmail usuario #{user_idx} (o 'fin'): ").strip()
                    if email_in.lower() == "fin" or email_in.lower() == "salir":
                        break
                    
                    is_admin_in = input(f"¿Es Administrador usuario #{user_idx}? (s/n): ").strip().lower()
                    is_admin = is_admin_in in ("s", "si", "sí", "y", "yes")

                    prompt_msg = f"Contraseña usuario #{user_idx} (opcional para admin): " if is_admin else f"Contraseña usuario #{user_idx}: "
                    pwd_in = getpass.getpass(prompt=prompt_msg)
                    if pwd_in.strip().lower() == "salir":
                        break
                    
                    user_manager.add_user(User(email=email_in, password=pwd_in, is_admin=is_admin))
                    user_idx += 1

                if user_manager.users:
                    batch_res = user_manager.validate_all()
                    print_batch_result(batch_res)
                else:
                    print("No se ingresaron usuarios para validar.\n")

            else:
                print(f"{COLOR_YELLOW}Opción no válida. Por favor elige 1, 2, 3 o 4.{COLOR_RESET}\n")

        except (KeyboardInterrupt, EOFError):
            print("\n¡Hasta luego!")
            break


def main() -> None:
    """Punto de entrada principal de la CLI."""
    pwd_validator = PasswordValidator()
    email_validator = EmailValidator()

    args = sys.argv[1:]
    if len(args) == 1:
        arg = args[0]
        if "@" in arg:
            # Auto-detectar validación de email
            res = email_validator.validate(arg)
            print_email_result(res)
            if not res.is_valid:
                sys.exit(1)
        else:
            # Validación de contraseña
            res = pwd_validator.validate(arg)
            print_password_result(res)
            if not res.is_valid:
                sys.exit(1)

    elif len(args) >= 2:
        # Si se pasan múltiples argumentos pares (email1, pwd1, email2, pwd2...)
        if len(args) % 2 == 0 and len(args) > 2:
            manager = UserManager(
                email_validator=email_validator,
                password_validator=pwd_validator
            )
            for i in range(0, len(args), 2):
                manager.add_user(User(email=args[i], password=args[i+1]))
            batch_res = manager.validate_all()
            print_batch_result(batch_res)
            if batch_res.invalid_users_count > 0:
                sys.exit(1)
        else:
            # Modo 1 solo par email + contraseña
            email_arg, pwd_arg = args[0], args[1]
            email_res = email_validator.validate(email_arg)
            print_email_result(email_res)

            pwd_res = pwd_validator.validate(pwd_arg, email=email_arg)
            print_password_result(pwd_res)

            if not (email_res.is_valid and pwd_res.is_valid):
                sys.exit(1)

    else:
        # Modo interactivo
        interactive_mode(pwd_validator, email_validator)


if __name__ == "__main__":
    main()

