import requests
from day_4.lib.base_case import BaseCase
from day_4.lib.assersions import Assertions as AS


class TestUserRegister(BaseCase):

    URL = "https://playground.learnqa.ru/api/user/"

    def test_create_user_successfully(self):
        data = self.prepare_registration_data()
        response = requests.post(self.URL, data=data)
        AS.assert_code_status(response, 200)
        AS.assert_json_has_key(response, "id")


    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)
        response = requests.post(self.URL, data=data)
        AS.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists",\
            f"Unexpected response content {response.content}"

