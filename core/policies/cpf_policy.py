import re


class CPFPolicy:
    @staticmethod
    def validate(cpf: str) -> str:
        cpf = re.sub(r"\D", "", cpf)

        if len(cpf) != 11:
            raise ValueError("CPF inválido")

        if cpf == cpf[0] * 11:
            raise ValueError("CPF inválido")

        def calc_digit(cpf, weight):
            total = sum(int(d) * w for d, w in zip(cpf, weight))
            rest = total % 11
            return "0" if rest < 2 else str(11 - rest)

        digit1 = calc_digit(cpf[:9], range(10, 1, -1))
        digit2 = calc_digit(cpf[:10], range(11, 1, -1))

        if cpf[-2:] != digit1 + digit2:
            raise ValueError("CPF inválido")

        return cpf
