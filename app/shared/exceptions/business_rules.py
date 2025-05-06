# app/shared/exceptions/business_rules.py

class RegraNegocioException(Exception):
    """
    Exceção base para violação de regras de negócio no EasyERP.
    """

    def __init__(self, mensagem="Violação de regra de negócio"):
        super().__init__(mensagem)
        self.mensagem = mensagem

    def to_dict(self):
        return {
            "erro": "regra_negocio",
            "mensagem": self.mensagem
        }


class ContaComSaldoException(RegraNegocioException):
    def __init__(self):
        super().__init__("A conta possui saldo diferente de zero e não pode ser removida.")


class ClienteInexistenteException(RegraNegocioException):
    def __init__(self):
        super().__init__("O cliente informado não existe.")


class EstoqueInsuficienteException(RegraNegocioException):
    def __init__(self):
        super().__init__("Quantidade insuficiente em estoque para realizar a movimentação.")


class OportunidadeSemProdutosException(RegraNegocioException):
    def __init__(self):
        super().__init__("A oportunidade deve conter ao menos um produto associado.")


class PermissaoNegadaException(RegraNegocioException):
    def __init__(self):
        super().__init__("Você não tem permissão para executar esta ação.")
