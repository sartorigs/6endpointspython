from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from random import randint

app = FastAPI()

clientes = [
    {
        "id": 1,
        "nome": "Silvio Santos",
        "valor_na_conta": 10000,
        "transacoes": [
            {
                "id": 1,
                "valor": 1500,
                "tipo": "d",
                "descricao": "Uma transacao",
            }
        ],
    },
    {
        "id": 2,
        "nome": "Fausto Silva",
        "valor_na_conta": 10,
        "transacoes": [
            {
                "id": 2,
                "valor": 1500,
                "tipo": "c",
                "descricao": "Uma transacao",
            },
            {
                "id": 3,
                "valor": 32,
                "tipo": "d",
                "descricao": "Uma transacao",
            },
        ],
    },
    {
        "id": 3,
        "nome": "Gugu Liberato",
        "transacoes": [],
    },
]

class Transacao(BaseModel):
    valor: float
    tipo: str
    descricao: str = None

def ObterCliente(id: int):
    for cliente in clientes:
        if cliente["id"] == id:
            return cliente
    return None

def GerarId():
    while True:
        novo_id = randint(10000, 99999)
        if not any(transacao["id"] == novo_id for cliente in clientes for transacao in cliente["transacoes"]):
            return novo_id

def ObterTransacao(cliente, transacao_id: int):
    for transacao in cliente["transacoes"]:
        if transacao["id"] == transacao_id:
            return transacao
    return None


@app.post("/clientes/{id}/transacoes")
async def criar_transacao(id: int, transacao: Transacao = Body(...)):
    cliente = ObterCliente(id)

    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    if transacao.tipo not in ("c", "d"):
        raise HTTPException(status_code=400, detail="Tipo de transação inválido")

    nova_transacao = {
        "id": GerarId(),
        **transacao.dict(),
    }

    cliente["transacoes"].append(nova_transacao)

    return nova_transacao

@app.get("/clientes/{id}/transacoes")
async def obter_transacoes(id: int):
    cliente = ObterCliente(id)

    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    return cliente["transacoes"]

@app.get("/clientes/{id}/transacoes/{transacao_id}")
async def obter_transacao(id: int, transacao_id: int):
    cliente = ObterCliente(id)

    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    transacao = ObterTransacao(cliente, transacao_id)

    if not transacao:
        raise HTTPException(status_code=404, detail="Transação não encontrada")

    return transacao

@app.put("/clientes/{id}/transacoes/{transacao_id}")
async def atualizar_transacao(
    id: int, transacao_id: int, transacao: Transacao = Body(...)
):
    cliente = ObterCliente(id)

    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    transacao_atualizada = ObterTransacao(cliente, transacao_id)

    if not transacao_atualizada:
        raise HTTPException(status_code=404, detail="Transação não encontrada")

    if transacao.tipo not in ("c", "d"):
        raise HTTPException(status_code=400, detail="Tipo de transação inválido")

    transacao_atualizada.update(**transacao.dict())

    return transacao_atualizada

@app.delete("/clientes/{id}/transacoes/{transacao_id}", status_code=204)
async def excluir_transacao(id: int, transacao_id: int):
    cliente = ObterCliente(id)

    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    transacao = ObterTransacao(cliente, transacao_id)

    if not transacao:
        raise HTTPException(status_code=404, detail="Transação não encontrada")

    cliente["transacoes"].remove(transacao)

    return

@app.get("/clientes/{id}")
async def obter_cliente(id: int):
    cliente = ObterCliente(id)

    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    return cliente





