import requests

class TestFirstAPI:

    def test_hello_call(self, names):
        name = names
        URL = "https://playground.learnqa.ru/api/hello"
        data = {'name': name}
        response = requests.get(URL, params=data)
        assert response.status_code == 200, "Wrong response code"
        response_dict = response.json()
        assert "answer" in response_dict, "There is no field 'answer' in the response"
        if len(name) == 0:
            expected_response_text = "Hello, someone"
        else:
            expected_response_text = f"Hello, {name}"
        actual_response_text = response_dict["answer"]
        assert actual_response_text == expected_response_text, 'Actual text in the response is not correct'


