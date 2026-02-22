import re


class PasswordPolicy:
    MIN_LENGTH = 8

    @staticmethod
    def validate(password: str) -> None:
        if len(password) < PasswordPolicy.MIN_LENGTH:
            raise ValueError("Senha deve ter no mínimo 8 caracteres")

        if " " in password:
            raise ValueError("Senha não pode conter espaços")

        rules = {
            "maiúscula": r"[A-Z]",
            "minúscula": r"[a-z]",
            "número": r"\d",
            "símbolo": r"[!@#$%^&*(),.?\":{}|<>]"
        }

        for nome, pattern in rules.items():
            if not re.search(pattern, password):
                raise ValueError(f"Senha deve conter pelo menos um {nome}")
