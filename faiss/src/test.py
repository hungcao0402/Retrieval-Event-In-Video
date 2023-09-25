import requests

def text_query(url, text, topk=10):
    
    params = {
        'text_query': text,
        'topk': 10
    }
    headers = {
        'accept': 'application/json'
    }

    response = requests.post(url, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()
        print(data)
    else:
        print(f"Request failed with status code: {response.status_code}")
        print(response.text)
        
url = 'http://localhost:8050/text_query'
text_query(url, 'a man with red hat', topk=10)