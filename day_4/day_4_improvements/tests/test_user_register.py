import pytest
import allure

from day_4.day_4_improvements.lib.base_case import BaseCase
from day_4.day_4_improvements.lib.assersions import Assertions as AS
from day_4.day_4_improvements.lib.my_requests import MyRequests as MR
from datetime import datetime as dt


@allure.epic("User Registration cases")
class TestUserRegister(BaseCase):

    URI = "/user/"
    params = [('firstName'), ('lastName'), ('username'), ('password'), ('email')]

    @allure.feature("User Registration")
    @allure.story("positive - Register new user")
    @allure.description("Verifiying that new user can be registered")
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()
        response = MR.post(self.URI, data=data)
        AS.assert_code_status(response, 200)
        AS.assert_json_has_key(response, "id")

    @allure.feature("User Registration")
    @allure.story("negative - Register user with already existing 'email'")
    @allure.description("Verifiying that new user can not be registered with existing 'email'")
    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)
        response = MR.post(self.URI, data=data)
        AS.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists",\
            f"Unexpected response content {response.content}"

    @allure.feature("User Registration")
    @allure.story("negative - Register user with wrong format 'email'")
    @allure.description("Verifiying that new user can not be registered with wrong format 'email'")
    def test_create_user_with_wrong_email(self):
        email = 'vinkotov.example.com'
        data = self.prepare_registration_data(email)
        response = MR.post(self.URI, data=data)
        AS.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Invalid email format", \
            f"Unexpected response content {response.content}"

    @allure.feature("User Registration")
    @allure.story("negative - Register user with missing 'data parameter'")
    @allure.description("Verifiying that new user can not be registered with missing 'data parameter'")
    @pytest.mark.parametrize("data_parameter", params)
    def test_create_user_with_missing_data_parameter(self, data_parameter):
        data = self.prepare_registration_data(missing_param=data_parameter)
        response = MR.post(self.URI, data=data)
        AS.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The following required params are missed: {data_parameter}", \
            f"Unexpected response content {response.content}"

    @allure.feature("User Registration")
    @allure.story("negative - Register user with empty 'data parameter'")
    @allure.description("Verifiying that new user can not be registered with empty 'data parameter'")
    @pytest.mark.parametrize("data_parameter", params)
    def test_create_user_with_empty_data_parameter(self, data_parameter):
        data = self.prepare_registration_data(empty_param=data_parameter)
        response = MR.post(self.URI, data=data)
        AS.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of '{data_parameter}' field is too short", \
            f"Unexpected response content {response.content}"

    @allure.feature("User Registration")
    @allure.story("negative - Register user with short 'first name'")
    @allure.description("Verifiying that new user can not be registered with short 'first name'")
    def test_create_user_with_short_name(self):
        email = 'v'
        data = self.prepare_registration_data(email)
        response = MR.post(self.URI, data=data)
        AS.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'email' field is too short", \
            f"Unexpected response content {response.content}"

    @allure.feature("User Registration")
    @allure.story("negative - Register user with very long 'first name'")
    @allure.description("Verifiying that new user can not be registered with very long 'first name'")
    def test_create_user_with_long_name(self):
        base_part = "learnqa" * 40
        domain = "example.com"
        random_part = dt.now().strftime("%m%d%Y%H%M%S")
        email = f"{base_part}{random_part}@{domain}"
        data = self.prepare_registration_data(email)
        response = MR.post(self.URI, data=data)
        AS.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'email' field is too long", \
            f"Unexpected response content {response.content}"

