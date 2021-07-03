import requests
from json.decoder import JSONDecodeError
from json_parsing import create_json_data


URL = "https://playground.learnqa.ru/api/hello"
URL2 = "https://playground.learnqa.ru/api/get_text"
URL3 = "https://playground.learnqa.ru/api/check_type"
URL4 = "https://playground.learnqa.ru/api/get_500"
URL5 = "https://playground.learnqa.ru/api/something"  # Not existing endpoint
URL6 = "https://playground.learnqa.ru/api/get_301"
URL7 = "https://playground.learnqa.ru/api/show_all_headers"
URL8 = "https://playground.learnqa.ru/api/get_auth_cookie"
URL9 = "https://playground.learnqa.ru/api/check_auth_cookie"
payload = {"name": "User"}
payload2 = {"login": "secret_login", "password": "secret_pass"}
payload3 = {"login": "secret_login", "password": "secret_pass2"}

response = requests.get(URL, params=payload)
response2 = requests.get(URL2)
response3 = requests.get(URL3, params=payload)
response4 = requests.post(URL3, data=payload)
response5 = requests.delete(URL3)
response6 = requests.put(URL3)
response7 = requests.put(URL4)
response8 = requests.put(URL5)
response9 = requests.get(URL6, allow_redirects=True)
response10 = requests.get(URL7, headers=payload)
response11 = requests.post(URL8, data=payload2)
response12 = requests.post(URL8, data=payload)
response14 = requests.post(URL8, data=payload3)


#################  Parsing JSON 1 ######################
print("#"*30,"Parsing JSON 1","#"*30)
data = create_json_data()
print(data['answer'])
print(data.get("answer"))

#################  Parsing JSON 2 ######################
print("#"*30,"Parsing JSON 2","#"*30)
parsed_response_text = response.json()
print(parsed_response_text.get("answer"))

print(response2.text)
try:
    parsed_response_text2 = response2.json()
    print(parsed_response_text2.get("answer"))
except JSONDecodeError:
    print("Response is not a JSON format")

####################  Check Type  #######################
print("#"*30,"Check Type","#"*30)
print(response3.text)
print(response4.text)
print(response5.text)
print(response6.text)


#####################  Server Codes ######################
print("#"*30,"Server Codes","#"*30)
print(response3.status_code)
print(response7.status_code)
print(response7.text)
print(response8.status_code)
print(response8.text)
print("#"*70)

first_response_9 = response9.history[0]
second_response_9 = response9
print(f"This is first response of 9 request {first_response_9}")
print(f"This is first response url of 9 request {first_response_9.url}")
print(f"This is second response of 9 request {second_response_9}")
print(f"This is second response url of 9 request {second_response_9.url}")


#####################  Headers ######################
print("#"*30,"Headers","#"*30)
print(response10.text)
print(response10.headers)


#####################  Cookies ######################
print("#"*30,"Cookies","#"*30)
print(response11.text)
print(response11.status_code)
print(response11.cookies)
print(dict(response11.cookies))
print(response11.headers)
print("#"*20,"wrong data","#"*20)
print(response12.text)
print(response12.status_code)
print(response12.cookies)
print(dict(response12.cookies))
print("#"*20,"pass valid cookie to get request","#"*20)
cookie_value = response11.cookies.get('auth_cookie')
cookies = {}
if cookies is not None:
    cookies.update({'auth_cookie': cookie_value})
response13 = requests.post(URL9, cookies = cookies)
print(response13.text)

print("#"*20,"pass valid cookie to get reques with wrong pass","#"*20)

cookie_value = response14.cookies.get('auth_cookie')
cookies = {}
if cookies is not None:
    cookies.update({'auth_cookie': cookie_value})
response13 = requests.post(URL9, cookies = cookies)
print(response13.text)