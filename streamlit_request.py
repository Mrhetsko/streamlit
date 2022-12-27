import os
import requests
import streamlit

a = os.getenv('csrftoken')
streamlit.write
cookies = {
    'csrftoken': os.getenv('csrftoken'),
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'uk,uk-UA;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    # 'Cookie': 'csrftoken=46e35PAmMK0cYF5zOJx2nLBEkYkhzSMEHUy0yhOmTrPNWKgL5RCpsuwT2OmMLgYo',
    'DNT': '1',
    'Origin': 'https://dmytro66.pythonanywhere.com',
    'Referer': 'https://dmytro66.pythonanywhere.com/',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

data = {
    'csrfmiddlewaretoken': os.getenv('csrfmiddlewaretoken'),
    'bucket_path': 'dfgsdfg',
}

response = requests.post('https://dmytro66.pythonanywhere.com/', cookies=cookies, headers=headers, data=data)
print(response.text)