import requests

url = 'http://127.0.0.1:8000/api/investments/'
headers = {
    'Authorization': 'c8664c9803ccd7b4a03653ea03e76a0136140088',
}

response = requests.get(url, headers=headers)
print(response.json())
