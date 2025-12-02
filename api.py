from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# -----------------------------
# Função para executar consultas
# -----------------------------
def query_db(query, args=(), one=False):
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cur = conn.execute(query, args)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return (rows[0] if rows else None) if one else rows


# -----------------------------
# Função principal da API
# -----------------------------
@app.route('/webservice/v1/fn_areceber', methods=['GET'])
def listar():

    # Parâmetros recebidos
    qtype      = request.args.get('qtype', 'id')           # coluna filtrada
    query_val  = request.args.get('query', '')             # valor da busca
    oper       = request.args.get('oper', 'like')          # operador (=, <, >, like)
    page       = int(request.args.get('page', 1))          # página
    rp         = int(request.args.get('rp', 20))           # registros por página
    sortname   = request.args.get('sortname', 'id')        # coluna de ordenação
    sortorder  = request.args.get('sortorder', 'asc')      # ordem

    # Mapeamento dos operadores da API
    operadores_validos = {
        '=': '=',
        '>': '>',
        '<': '<',
        'like': 'LIKE'
    }

    if oper not in operadores_validos:
        return jsonify({"error": "Operador inválido"}), 400

    # Construir filtro SQL
    if oper == 'like':
        filtro = f"{qtype} LIKE ?"
        valor = f"%{query_val}%"
    else:
        filtro = f"{qtype} {operadores_validos[oper]} ?"
        valor = query_val

    # Paginação
    offset = (page - 1) * rp

    # SQL final
    sql = f"""
        SELECT *
        FROM fn_areceber
        WHERE {filtro}
        ORDER BY {sortname} {sortorder}
        LIMIT ? OFFSET ?
    """

    resultados = query_db(sql, (valor, rp, offset))

    # Transformar em JSON padrão IXC
    lista = [dict(row) for row in resultados]

    resposta = {
        "page": page,
        "total": len(lista),
        "rows": lista
    }

    return jsonify(resposta)


# -----------------------------
# Inicializar servidor
# -----------------------------
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

