import allure
from day_4.day_4_improvements.lib.base_case import BaseCase
from day_4.day_4_improvements.lib.assersions import Assertions as AS
from day_4.day_4_improvements.lib.my_requests import MyRequests as MR


@allure.epic("User Profile View cases")
class TestUserGet(BaseCase):
    BASE_URI: str = "/user/"

    @allure.feature("User Profile View")
    @allure.story("negative - View user profile details without authorization")
    @allure.description("Verifiying that only user 'username' can be viewed without authorization")
    def test_get_user_details_not_auth(self):
        user_id = "2"
        URI = self.BASE_URI + user_id
        response = MR.get(URI)
        AS.assert_json_has_key(response, "username")
        expected_fields = ["email", "firstName", "lastName"]
        AS.assert_json_has_no_keys(response, expected_fields)

    @allure.feature("User Profile View")
    @allure.story("positive - View user profile details with authorization")
    @allure.description("Verifiying that user profile details' can be viewed with authorization")
    def test_get_user_details_auth_as_same_user(self):
        URI1 = self.BASE_URI + "login"
        user_email = "vinkotov@example.com"
        user_password = "1234"
        data = {
            'email': user_email,
            'password': user_password
        }
        response1 = MR.post(URI1, data=data)
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        URI2 = self.BASE_URI + str(user_id_from_auth_method)
        headers = {
            'x-csrf-token': token
        }
        cookies = {
            'auth_sid': auth_sid
        }
        response2 = MR.get(URI2, headers=headers, cookies=cookies)
        expected_fields = ["id", "username", "email", "firstName", "lastName"]
        AS.assert_json_has_keys(response2, expected_fields)

    @allure.feature("User Profile View")
    @allure.story("negative - View user profile details with another user authorization")
    @allure.description("Verifiying that only user 'username' can be viewed with another user authorization")
    def test_get_user_details_with_auth_as_another_user(self):
        URI1 = self.BASE_URI + "login"
        user_email = "vinkotov@example.com"
        user_password = "1234"
        data = {
            'email': user_email,
            'password': user_password
        }
        response1 = MR.post(URI1, data=data)
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        URI2 = self.BASE_URI + str(user_id_from_auth_method - 1)
        headers = {
            'x-csrf-token': token
        }
        cookies = {
            'auth_sid': auth_sid
        }
        response2 = MR.get(URI2, headers=headers, cookies=cookies)

        expected_fields = ["username"]
        unexpected_fields = ["id", "email", "firstName", "lastName"]

        AS.assert_json_has_keys(response2, expected_fields)
        AS.assert_json_has_no_keys(response2, unexpected_fields)
