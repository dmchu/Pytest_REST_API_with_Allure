import requests

class TestFirstAPI:
    def test_hello_call(self):
        URL = "https://playground.learnqa.ru/api/hello"
        name = "Vitalik"
        data = {'name': name}
        response = requests.get(URL, params=data)
        response.raise_for_status()
        response_dict = response.json()
        assert "answer" in response_dict, "There is no field 'answer' in the response"

        expected_response_text = f"Hello, {name}"
        actual_response_text = response_dict["answer"]
        assert actual_response_text == expected_response_text, 'Actual text in the response is not correct'