import requests
from day_4.lib.base_case import BaseCase
from day_4.lib.assersions import Assertions as AS


class TestUserEdit(BaseCase):

    BASE_URL: str = "https://playground.learnqa.ru/api/user/"

    def test_edit_just_created_user(self):
        # Registration
        register_data = self.prepare_registration_data()
        response1 = requests.post(self.BASE_URL, data=register_data)
        AS.assert_code_status(response1, 200)
        AS.assert_json_has_key(response1, "id")
        user_email = register_data.get("email")
        first_name = register_data.get("firstName")
        user_password = register_data.get("password")
        user_id = self.get_json_value(response1, "id")

        # Authorization
        login_data = {
            'email': user_email,
            'password': user_password
        }

        URL1 = self.BASE_URL + "login"

        response2 = requests.post(URL1, data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        URL2 = self.BASE_URL + str(user_id)
        new_name = "Changed Name"
        headers = {
            'x-csrf-token': token
        }
        cookies = {
            'auth_sid': auth_sid
        }
        edit_data = {
            'firstName': new_name
        }
        # Edit user data

        response3 = requests.put(URL2, headers=headers, cookies=cookies, data=edit_data)
        AS.assert_code_status(response3, 200)
        # expected_fields = ["username", "email", "firstName", "lastName"]
        # AS.assert_json_has_keys(response3, expected_fields)

        # Get updated user data

        response4 = requests.get(URL2, headers=headers, cookies=cookies)
        AS.assert_json_value_by_name(response4, "firstName", new_name, "Wrong name of user after update")