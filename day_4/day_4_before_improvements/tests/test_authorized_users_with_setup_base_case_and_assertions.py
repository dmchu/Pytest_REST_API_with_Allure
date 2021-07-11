import requests
import pytest
from day_4.day_4_before_improvements.lib.base_case import BaseCase
from day_4.day_4_before_improvements.lib.assersions import Assertions as AS

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
        error_message = "User id from auth method is not equal to user id from check method"
        AS.assert_json_value_by_name(response2, "user_id", self.user_id_from_auth_method, error_message)

    @pytest.mark.parametrize("condition", exclude_params)
    def test_negative_auth_chech(self, condition):
        if condition == "no_cookie":
            response2 = requests.get(self.URL2, headers=self.auth_headers)
        else:
            response2 = requests.get(self.URL2, cookies=self.auth_cookies)

        error_message = f"User is authorized with condition {condition}"
        AS.assert_json_value_by_name(response2, "user_id", 0, error_message)
