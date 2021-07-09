import requests
import pytest

class TestUserAuth:
    def test_auth_user(self):
        URL1 = "https://playground.learnqa.ru/api/user/login"
        URL2 = "https://playground.learnqa.ru/api/user/auth"

        payload_1 = {
            'email':'vinkotov@example.com',
            'password':'1234'
        }

        response1 = requests.post(URL1, data=payload_1)

        assert "auth_sid" in response1.cookies, "There is no auth cookie in the response"
        assert "x-csrf-token" in response1.headers, "There is no CSRF token header in the response"
        assert "user_id" in response1.json(), "There is no user id in the response"

        auth_sid = response1.cookies.get("auth_sid")
        token = response1.headers.get("x-csrf-token")
        user_id_from_auth_method = response1.json()["user_id"]
        auth_headers = {
            "x-csrf-token": token,
        }
        auth_cookies = {
            "auth_sid": auth_sid
        }
        response2 = requests.get(URL2,headers=auth_headers, cookies=auth_cookies)

        assert "user_id" in response2.json(), "There is no user id in the second response"

        user_id_from_check_method = response2.json()["user_id"]

        assert user_id_from_auth_method == user_id_from_check_method,\
            "User id from auth method is not equal to user id from check method"

    exclude_params = [("no_cookie"), ("no_tocken")]

    @pytest.mark.parametrize("condition", exclude_params)
    def test_negative_auth_chech(self, condition):
        URL1 = "https://playground.learnqa.ru/api/user/login"
        URL2 = "https://playground.learnqa.ru/api/user/auth"

        payload_1 = {
            'email':'vinkotov@example.com',
            'password':'1234'
        }

        response1 = requests.post(URL1, data=payload_1)

        assert "auth_sid" in response1.cookies, "There is no auth cookie in the response"
        assert "x-csrf-token" in response1.headers, "There is no CSRF token header in the response"
        assert "user_id" in response1.json(), "There is no user id in the response"

        auth_sid = response1.cookies.get("auth_sid")
        token = response1.headers.get("x-csrf-token")

        auth_headers = {
            "x-csrf-token": token,
        }
        auth_cookies = {
            "auth_sid": auth_sid
        }

        if condition == "no_cookie":
            response2 = requests.get(URL2, headers=auth_headers)
        else:
            response2 = requests.get(URL2, cookies=auth_cookies)

        assert "user_id" in response2.json(), "There is no user id in the second response"
        user_id_from_check_method = response2.json().get("user_id")
        assert user_id_from_check_method == 0, f"User is authorized with condition {condition}"