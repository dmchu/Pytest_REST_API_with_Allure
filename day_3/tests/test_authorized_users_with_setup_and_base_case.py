import requests
import pytest
from day_3.lib.base_case import BaseCase

class TestUserAuth(BaseCase):

    exclude_params = [("no_cookie"), ("no_tocken")]

    def setup(self):
        self.URL1 = "https://playground.learnqa.ru/api/user/login"
        self.URL2 = "https://playground.learnqa.ru/api/user/auth"
        self.payload_1 = {
            'email':'vinkotov@example.com',
            'password':'1234'
        }
        response1 = requests.post(self.URL1, data=self.payload_1)
        self.auth_sid = self.get_cookie(response1, "auth_sid")
        self.token = self.get_header(response1, "x-csrf-token")
        self.user_id_from_auth_method = self.get_json_value(response1, "user_id")
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