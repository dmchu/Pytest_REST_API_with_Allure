import requests
from day_4.day_4_before_improvements.lib.base_case import BaseCase
from day_4.day_4_before_improvements.lib.assersions import Assertions as AS


class TestUserGet(BaseCase):

    BASE_URL: str = "https://playground.learnqa.ru/api/user/"

    def test_get_user_details_not_auth(self):
        user_id = "2"
        URL = self.BASE_URL + user_id
        response = requests.get(URL)
        AS.assert_json_has_key(response, "username")
        expected_fields = ["email", "firstName", "lastName"]
        AS.assert_json_has_no_keys(response, expected_fields)

    def test_get_user_details_auth_as_same_user(self):
        URL1 = self.BASE_URL + "login"
        user_email = "vinkotov@example.com"
        user_password = "1234"
        data = {
            'email': user_email,
            'password': user_password
        }
        response1 = requests.post(URL1, data=data)
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        URL2 = self.BASE_URL + str(user_id_from_auth_method)
        headers = {
            'x-csrf-token': token
        }
        cookies = {
            'auth_sid': auth_sid
        }
        response2 = requests.get(URL2, headers=headers, cookies=cookies)
        expected_fields = ["username", "email", "firstName", "lastName"]
        AS.assert_json_has_keys(response2, expected_fields)
