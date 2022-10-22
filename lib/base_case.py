from requests import Response
import json.decoder


class BaseCase:
    def get_header(self, response: Response, headers_name):
        assert headers_name in response.headers, f"Cannot find header with the name {headers_name} in the last response"
        return response.headers[headers_name]

    def get_json_value(self, response: Response, name):
        try:
            response_as_dict = response.json() #парсинг JSON ответ в dictionary Python
        except json.decoder.JSONDecoderError:
            assert False, f"Response isn't JSON format. Response text is '{response.text}'"

        assert name in response_as_dict, f"Response JSON doesn't have key '{name}'"
        return response_as_dict[name]