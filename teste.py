import requests

url = "http://localhost:5000/webservice/v1/cliente_contrato"

payload = {
    'qtype': 'id',
    'query': '0',
    'oper': '>',
    'page': '1',
    'rp': '20',
    'sortname': 'id',
    'sortorder': 'asc'
}

headers = {
    'Content-Type': 'application/json'
}

response = requests.get(url, params=payload, headers=headers)

print("Status:", response.status_code)
print("Resposta JSON:")
print(response.json())