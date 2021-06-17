import requests

URL = "https://playground.learnqa.ru/api/get_text"

response = requests.get(URL)
print(response.text)