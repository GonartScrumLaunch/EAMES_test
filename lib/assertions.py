from requests import Response
import json


class Assertions:
    """Compare the actual status code with the expected status code"""
    @staticmethod
    def assert_code_status(response: Response, expected_status_code):
        assert response.status_code == expected_status_code,\
            f"Unexpected status code. Expected result: {expected_status_code}. Actual result: {response.status_code}"

    """Method for checking if required fields are in JSON response"""
    @staticmethod
    def checking_required_field(response: Response, expected_field):
        response_json = json.loads(response.text)
        assert list(response_json) == expected_field, f"Actual result: {list(response_json)} doesn't correspond to " \
                                                      f"expected result: {expected_field}"

    """Method for checking if key value exists in JSON response"""
    @staticmethod
    def checking_required_value(response: Response, field_name, expected_value):
        check_json = response.json()
        check_value = check_json.get(field_name)
        assert str(check_value) == expected_value, f"Actual result: {check_value} doesn't correspond to " \
                                                   f"expected result: {expected_value}"

    # @staticmethod
    # def assert_json_value_has_key(response: Response, name):
    #     try:
    #         response_as_dict = response.json()
    #     except json.decoder.JSONDecodeError:
    #         assert False, f"Response isn't in JSON format. Response text is '{response.text}'"
    #     assert name in response_as_dict, f"Response JSON doesn't have key '{name}'"
    
