import asyncio
import requests
from mcp.server.fastmcp import FastMCP

# Nome do servidor MCP
app = FastMCP("api-wrapper")

# URL base da sua API Flask
BASE_URL = "http://localhost:5000/webservice/v1"

# ----------------------------
# Endpoints permitidos (WHITELIST)
# ----------------------------
ENDPOINTS_PERMITIDOS = {
    "fn_areceber",   # adicione somente se necessário
}


# ============================================================
# TOOL 1: consultar — estilo IXC (com paginação e filtros)
# ============================================================
@app.tool()
async def consultar(
    endpoint: str,
    qtype: str,
    query: str,
    oper: str = "=",
    page: int = 1,
    rp: int = 20,
    sortname: str = "id",
    sortorder: str = "asc"
) -> dict:
    """
    Executa uma consulta na API Flask no estilo IXC.

    Parâmetros
    ----------
    endpoint : str
        Nome do recurso autorizado. Ex: "fn_areceber".
        Apenas endpoints presentes no whitelist podem ser usados.

    qtype : str
        Nome do campo pelo qual a consulta será filtrada.
        Exemplo: "id", "nome_cliente", "cpf", "id_contrato".

    query : str
        Valor da busca, combinado com o operador.
        Exemplo: "123", "JOAO", "1050".

    oper : str
        Operador lógico.
        Permitidos: "=", ">", "<", ">=", "<=", "like".
        Default: "=".

    page : int
        Página da consulta (paginação).
        Default: 1.

    rp : int
        Quantidade de registros por página.
        Default: 20.

    sortname : str
        Campo de ordenação.
        Exemplo: "id", "data_cadastro".

    sortorder : str
        Ordem: "asc" ou "desc".
        Default: "asc".

    Retorno
    -------
    dict
        JSON retornado pela API Flask correspondente ao endpoint.
    """

    # Segurança: bloqueia endpoints não permitidos
    if endpoint not in ENDPOINTS_PERMITIDOS:
        raise ValueError(f"Endpoint '{endpoint}' não permitido.")

    # Segurança: bloqueia operadores arriscados
    OPERADORES_SEGUROS = {"=", ">", "<", ">=", "<=", "like"}
    if oper not in OPERADORES_SEGUROS:
        raise ValueError(f"Operador '{oper}' não permitido.")

    url = f"{BASE_URL}/{endpoint}"

    params = {
        "qtype": qtype,
        "query": query,
        "oper": oper,
        "page": page,
        "rp": rp,
        "sortname": sortname,
        "sortorder": sortorder
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()




# ============================================================
# Rodar o MCP Server
# ============================================================
if __name__ == "__main__":
    asyncio.run(app.run())
