from requests import Response
import json.decoder
from datetime import datetime

"""class of basic functions for multiple use in tests"""
class BaseCase:
    def get_header(self, response: Response, headers_name):
        assert headers_name in response.headers, f"Cannot find header with the name {headers_name} in the last response"
        return response.headers[headers_name]

    def get_json_value(self, response: Response, name):
        try:
            response_as_dict = response.json() # parsing JSON, response in dictionary Python
        except json.decoder.JSONDecoderError:
            assert False, f"Response isn't JSON format. Response text is '{response.text}'"

        assert name in response_as_dict, f"Response JSON doesn't have key '{name}'"
        return response_as_dict[name]

    """Method for adding current date to project name"""
    def project_name(self):
        base_name = "Test_project from "
        current_date = datetime.utcnow().strftime("%Y-%m-%d")
        current_date_to_sec = datetime.utcnow().strftime("%m-%d-%YT%H:%M:%S")
        project_name = f"{base_name}{current_date_to_sec}"
        return current_date, project_name, current_date_to_sec

