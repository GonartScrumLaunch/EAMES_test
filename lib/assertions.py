from requests import Response
import json


class Assertions:
    @staticmethod
    def assert_code_status(response: Response, expected_status_code):
        assert response.status_code == expected_status_code,\
            f"Unexpected status code. Expected: {expected_status_code}. Actual: {response.status_code}"

    """"@staticmethod
    def assert_json_value_has_key(response: Response, name):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response isn't in JSON format. Response text is '{response.text}'"
        assert name in response_as_dict, f"Response JSON doesn't have key '{name}'"""""
    
