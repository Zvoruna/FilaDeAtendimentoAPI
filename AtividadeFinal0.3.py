from fastapi import FastAPI, HTTPException,  status, Response
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

my_api = FastAPI()


# Modelo de Dados Pydantic
# https://fastapi.tiangolo.com/pt/tutorial/body/
class Cliente(BaseModel):
    posicaoFila: int
    nome: str = Field(None, max_length=20)
    # O campo nome é obrigatório e deve ter no máximo 20 caracteres;
    # Field https://pydantic-docs.helpmanual.io/usage/schema/#field-customization
    dataChegada: datetime = None
    atendido: bool = False
    id: int = 0
    tipoAtendimento: str = Field(None, max_length=1)
    # O campo tipo de atendimento só aceita 1 caractere (N ou P);



class ListaCliente(BaseModel):
    __root__: List[Cliente]


ListaCliente.parse_obj([
    {'posicaoFila': '1', 'nome': "Melissa", 'dataChegada': '2022-11-27 00:10', 'id': 1, 'tipoAtendimento': 'P'},
    {'posicaoFila': '2', 'nome': "Eli", 'dataChegada': '2022-11-27 00:11', 'id': 2, 'tipoAtendimento': 'N'},
   {'posicaoFila': '3', 'nome': "João", 'dataChegada': '2022-11-27 00:12', 'id': 3, 'tipoAtendimento': 'N'},
   {'posicaoFila': '4', 'nome': "Joana", 'dataChegada': '2022-11-27 00:13', 'id': 4, 'tipoAtendimento': 'P'},
 ])


# https://pydantic-docs.helpmanual.io/usage/models/#parsing-data-into-a-specified-type


# 1.Crie o endpoint GET /fila
@my_api.get("/fila")
async def get_cliente(cliente: Cliente):
    clientes = []
    for cliente in ListaCliente.__root__:
        if not cliente.atendido:
            clientes.append(cliente)
    if len(clientes) == 0:
        # ou length_hint()
        return {"Lista de fila: \n": "Não há Clientes"}
    # raise HTTPException(status_code=200, detail="Não há clientes na fila")
    # https://fastapi.tiangolo.com/tutorial/handling-errors/
    else:
        return {"Lista de fila: \n": clientes}
        # Exibir a posição na fila, o nome e a data de chegada de cada cliente não atendido que está na fila.


# 2.Crie o endpoint GET /fila/:id
@my_api.get("/fila/{id}")
async def get_cliente_id(id: int):
    clientes = []
    for Cliente in ListaCliente.__root__:
        if Cliente.id == id:
            clientes.append(Cliente)

    if len(clientes) > 0:
        return {"Lista de fila: \n": clientes}
    # Retornar os dados do cliente (posição na fila, o nome e a data de chegada) na posição (id) da fila.
    else:
        raise HTTPException(status_code=404, detail="Não há uma pessoa na posição especificada")
    # Se não tiver uma pessoa na posição especificada no id da rota deve ser retornado o status 404
    # e uma mensagem informativa no JSON de retorno;


# 3.Crie o endpoint POST /fila
@my_api.post("/fila")
async def adicionar_cliente(cliente: Cliente):
    cliente.nome = "Fulano"  # Nome Exemplo
    cliente.tipoAtendimento = "N"  # Tipo Exemplo

    cliente.posicao = ListaCliente.__root__[-1].posicaoFila + 1
    # Posição na Fila
    cliente.dataChegada = datetime.now()
    # Data de chegada
    cliente.atendido = False
    # Campo atendido
    cliente.id = ListaCliente.__root__[-1].id + 1
    ListaCliente.__root__.append(cliente)

    nome_exemplo = ListaCliente.__root__[-1].nome
    tipo_exemplo = ListaCliente.__root__[-1].tipoAtendimento
    return {"Cliente Adicionado: " + "Nome: " + nome_exemplo + " Tipo de Atendimento: " + tipo_exemplo}


# Adicionar um novo cliente na fila, informando seu nome e se o atendimento é normal (N) ou prioritário (P).
# Será identificada sua posição na fila, sua data de entrada e o campo atendido será setado como FALSE.


# 4.Crie o endpoint PUT /fila
@my_api.put("/fila")
async def atualizar_cliente():
    for Cliente in ListaCliente.__root__:
        if Cliente.posicaoFila == 1:
            Cliente.posicaoFila = 0
            Cliente.atendido = True
            # Caso o cliente esteja na posição 1 ele será atualizado para a posição 0
            # e o campo atendido será setado para TRUE.
        else:
            Cliente.posicaoFila -= 1
            # Será atualizada a posição de cada pessoa que está na fila (-1);
    return {"Lista de clientes atualizada"}


# 5. Crie o endpoint DELETE /fila/:id
@my_api.delete("/fila/{id}")
async def deletar_cliente(id: int):
    clientes = []
    for Cliente in ListaCliente.__root__:
        if Cliente.id == id:
            clientes.append(Cliente)

    if len(clientes) == 0:
        raise HTTPException(status_code=404, detail="Cliente não localizado na fila")
        # Caso o cliente não seja localizado na posição especificada no id da rota deve ser retornado o status 404
    else:
        ListaCliente.__root__.remove(clientes[id])
        return {"Cliente Removido da Lista"}

# cmd: python -m uvicorn AtividadeFinal:my_api --reload
