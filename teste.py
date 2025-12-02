import requests

url = "http://localhost:5000/webservice/v1/fn_areceber"

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

response = requests.post(url, params=payload, headers=headers)


print(response.json())

