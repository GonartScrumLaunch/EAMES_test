import datetime
import os
from requests import Response


class Logger:
    file_name = r'C:\Users\Legion\Desktop\EAMES_test\logs\log_' + str(datetime.datetime.utcnow().strftime("%m-%d-%Y_%H-%M-%S")) + '.log'

    @classmethod
    def _write_log_to_file(cls, data: str):
        with open(cls.file_name, 'a', encoding='utf-8') as logger_file:
            logger_file.write(data)

    @classmethod
    def add_request(cls, url: str, data: dict, headers: dict, method: str):
        test_name = os.environ.get("PYTEST_CURRENT_TEST")

        data_to_add = "\n----------\n"
        data_to_add += f"Test: {test_name}\n"
        data_to_add += f"Time: {str(datetime.datetime.utcnow())}\n"
        data_to_add += f"Request method: {method}\n"
        data_to_add += f"Request URL: {url}\n"
        data_to_add += f"Request data: {data}\n"
        data_to_add += f"Headers: {headers}\n"
        data_to_add += f"\n"

        cls._write_log_to_file(data_to_add)

    @classmethod
    def add_response(cls, response: Response):
        headers_as_dict = dict(response.headers)

        data_to_add = f"Response code: {response.status_code}\n"
        data_to_add += f"Response text: {response.text}\n"
        data_to_add += f"Response content: {response.content}\n"
        data_to_add += f"Response header: {headers_as_dict}\n"
        data_to_add += "----------\n"

        cls._write_log_to_file(data_to_add)
