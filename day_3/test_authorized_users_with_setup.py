import requests
import pytest

class TestUserAuth:

    exclude_params = [("no_cookie"), ("no_tocken")]

    def setup(self):
        self.URL1 = "https://playground.learnqa.ru/api/user/login"
        self.URL2 = "https://playground.learnqa.ru/api/user/auth"
        self.payload_1 = {
            'email':'vinkotov@example.com',
            'password':'1234'
        }
        response1 = requests.post(self.URL1, data=self.payload_1)

        assert "auth_sid" in response1.cookies, "There is no auth cookie in the response"
        assert "x-csrf-token" in response1.headers, "There is no CSRF token header in the response"
        assert "user_id" in response1.json(), "There is no user id in the response"

        self.auth_sid = response1.cookies.get("auth_sid")
        self.token = response1.headers.get("x-csrf-token")
        self.user_id_from_auth_method = response1.json()["user_id"]
        self.auth_headers = {
            "x-csrf-token": self.token,
        }
        self.auth_cookies = {
            "auth_sid": self.auth_sid
        }


    def test_auth_user(self):
        response2 = requests.get(self.URL2,headers=self.auth_headers, cookies=self.auth_cookies)
        assert "user_id" in response2.json(), "There is no user id in the second response"
        user_id_from_check_method = response2.json()["user_id"]
        assert self.user_id_from_auth_method == user_id_from_check_method,\
            "User id from auth method is not equal to user id from check method"



    @pytest.mark.parametrize("condition", exclude_params)
    def test_negative_auth_chech(self, condition):
        if condition == "no_cookie":
            response2 = requests.get(self.URL2, headers=self.auth_headers)
        else:
            response2 = requests.get(self.URL2, cookies=self.auth_cookies)

        assert "user_id" in response2.json(), "There is no user id in the second response"
        user_id_from_check_method = response2.json().get("user_id")
        assert user_id_from_check_method == 0, f"User is authorized with condition {condition}"