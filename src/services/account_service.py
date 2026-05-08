from sqlalchemy import select
from src.models.cliente import Cliente
from src.models.conta import Conta
from src.core.exceptions import NotFoundError, BusinessError
from src.security.password import verify_password, hash_password
from sqlalchemy.exc import IntegrityError


class AccountService:

    def __init__(self, account_repo):
        self.account_repo = account_repo

    async def buscar_cliente(self, db, cpf):
        return await self.account_repo.buscar_cliente_por_cpf(db, cpf)

    async def buscar_cliente_ou_erro(self, db, cpf):
        cliente = await self.buscar_cliente(db, cpf)

        if not cliente:
            raise NotFoundError("Cliente não encontrado")

        return cliente

    async def criar_usuario(self, db, data):
        cliente = await self.account_repo.buscar_cliente_por_cpf(db, data.cpf)

        if cliente:
            raise BusinessError("Usuário já existe")

        novo = Cliente(
            nome=data.nome,
            cpf=data.cpf,
            senha_hash=hash_password(data.senha),
            data_nascimento=data.data_nascimento,
            endereco=data.endereco
        )

        return await self.account_repo.criar_cliente(db, novo)

    async def criar_conta(self, db, cpf):
        cliente = await self.buscar_cliente_ou_erro(db, cpf)

        conta_existente = await self.account_repo.buscar_conta_por_cliente_id(db, cliente.id)

        if conta_existente:
            raise BusinessError("Cliente já possui conta")

        conta = Conta(cliente_id=cliente.id)

        try:
            return await self.account_repo.criar_conta(db, conta)
        except IntegrityError:
            raise BusinessError("Cliente já possui conta")

    async def obter_conta(self, db, user_id: int):
        conta = await self.account_repo.buscar_conta_por_cliente_id(db, user_id)

        if not conta:
            raise NotFoundError("Conta não encontrada")

        return conta

    async def autenticar(self, db, cpf: str, senha: str):
        cliente = await self.buscar_cliente(db, cpf)

        if not cliente:
            raise BusinessError("Credenciais inválidas")

        if not verify_password(senha, cliente.senha_hash):
            raise BusinessError("Credenciais inválidas")

        return cliente