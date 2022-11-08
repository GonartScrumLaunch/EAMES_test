import pytest
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure


@allure.epic("All tests")
class TestCreateProject(BaseCase):
    @pytest.fixture(autouse=True)  # access the pytest library and fixture means that the setup function will be executed before our tests are run
    def setup(self):
        x_app = {"X-Application": "eames"}
        payload = {"email": "test3@email.com",
                   "password": "123123"
                   }
        name = self.project_name()
        install_date = name[0]
        address = name[1]
        curr_date_to_sec = name[2]

        self.body_create_project = {
            "install_date": install_date,
            "address": address,
            "city": "Denver",
            "state": "Colorado",
            "zip": "80200"
            }
        self.body_add_room = {
            "name": "Room №" + str(curr_date_to_sec),
            "room_type": "Office",  # optional field to create a room
            "order": 1
            }

        response1 = MyRequests.post("/v1/users/authenticate", data=payload, headers=x_app)
        Assertions.assert_code_status(response1, 200)
        Assertions.checking_required_field(response1, ['success', 'user', 'tokens'])
        Assertions.checking_required_value(response1, 'success', 'True')
        self.token = self.get_json_value(response1, "tokens")["access_token"]
        self.client = self.get_json_value(response1, "tokens")["client"]
        self.user_id_after_auth = self.get_json_value(response1, "user")["id"]
        self.uid = self.get_header(response1, "uid")
        self.headers = {"client": self.client, "access_token": self.token, "uid": self.uid, "X-Application": "eames"}

    @allure.description("Checking user authorization with email and password")
    def test_user_auth(self):
        response2 = MyRequests.get("/v1/users", headers=self.headers)
        Assertions.assert_code_status(response2, 200)
        Assertions.checking_required_field(response2, ['success', 'user'])
        Assertions.checking_required_value(response2, 'success', 'True')
        assert "id" in response2.json()["user"], "No user_id in second response"
        user_id_with_same_uid_profile = response2.json()["user"]["id"]
        assert self.user_id_after_auth == user_id_with_same_uid_profile, f"User id: {self.user_id_after_auth} from " \
            f"first response doesn't match user id: {user_id_with_same_uid_profile} from second response"

    @allure.description("Create a project with valid data")
    def test_create_project_with_valid_data(self):
        response3 = MyRequests.post("/inventory/v1/projects", data=self.body_create_project, headers=self.headers)
        Assertions.assert_code_status(response3, 201)
        Assertions.checking_required_field(response3, ['data', 'success'])
        Assertions.checking_required_value(response3, 'success', 'True')

    @allure.description("Checking existence of created project")
    def test_check_existence_of_created_project(self):
        response3 = MyRequests.post("/inventory/v1/projects", data=self.body_create_project, headers=self.headers)
        Assertions.assert_code_status(response3, 201)
        Assertions.checking_required_field(response3, ['data', 'success'])
        Assertions.checking_required_value(response3, 'success', 'True')
        project_id = self.get_json_value(response3, 'data')['id']
        response4 = MyRequests.get(f"/inventory/v1/projects/{project_id}/project_info", headers=self.headers)
        Assertions.assert_code_status(response4, 200)
        Assertions.checking_required_field(response4, ['success', 'proejct'])
        Assertions.checking_required_value(response4, 'success', 'True')

    @allure.description("Adding room to project")
    def test_add_room_to_project(self):
        response3 = MyRequests.post("/inventory/v1/projects", data=self.body_create_project, headers=self.headers)
        Assertions.assert_code_status(response3, 201)
        Assertions.checking_required_field(response3, ['data', 'success'])
        Assertions.checking_required_value(response3, 'success', 'True')
        project_id = self.get_json_value(response3, 'data')['id']
        response5 = MyRequests.post(f'/inventory/v1/projects/{project_id}/rooms', headers=self.headers,
                                    data=self.body_add_room)
        Assertions.assert_code_status(response5, 201)
        Assertions.checking_required_field(response5, ['data', 'success'])
        Assertions.checking_required_value(response5, 'success', 'True')
