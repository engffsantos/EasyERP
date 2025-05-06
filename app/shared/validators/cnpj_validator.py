# app/shared/validators/cnpj_validator.py

import re


def validar_cnpj(cnpj: str) -> bool:
    """
    Valida um número de CNPJ (formato brasileiro).
    Retorna True se for válido, False caso contrário.
    """

    cnpj = re.sub(r'\D', '', cnpj)

    if len(cnpj) != 14 or cnpj == cnpj[0] * 14:
        return False

    def calcular_digito(cnpj_parcial, pesos):
        soma = sum(int(digito) * peso for digito, peso in zip(cnpj_parcial, pesos))
        resto = soma % 11
        return '0' if resto < 2 else str(11 - resto)

    # Primeiro dígito
    pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    digito1 = calcular_digito(cnpj[:12], pesos1)

    # Segundo dígito
    pesos2 = [6] + pesos1
    digito2 = calcular_digito(cnpj[:12] + digito1, pesos2)

    return cnpj[-2:] == digito1 + digito2


def formatar_cnpj(cnpj: str) -> str:
    """
    Formata um CNPJ limpo como 00.000.000/0000-00
    """
    cnpj = re.sub(r'\D', '', cnpj)
    if len(cnpj) != 14:
        return cnpj
    return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"
