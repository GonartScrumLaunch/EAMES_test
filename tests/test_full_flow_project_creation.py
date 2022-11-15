import pytest
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure
from environment import ENV_OBJECT


@allure.epic("All tests")
class TestCreateProject(BaseCase):
    @pytest.fixture(autouse=True)  # access the pytest library and fixture means that the setup
    # function will be executed before our tests are run
    def setup(self):
        self.x_app = {"X-Application": "eames"}

        if ENV_OBJECT.get_base_url() == 'https://api.byshowroom.com':
            self.payload = {"email": "testemailadmin@gmail.com",
                            "password": "giranrolll4"
                            }
        else:
            self.payload = {"email": "test3@email.com",
                            "password": "123123"
                            }

        name = self.project_name()
        install_date = name[0]
        address = name[1]
        self.curr_date_to_sec = name[2]
        self.body_with_required_field = {
            "install_date": install_date,
            "address": address,
            "city": "Denver",
            "state": "Colorado",
            "zip": "80200"
        }
        self.body_with_required_optional_field = {
            "install_date": install_date,
            "address": address,
            "city": "Denver",
            "state": "Colorado",
            "zip": "80200",
            "project_type": "Furniture Sale",
            "content_stage": "No Stage",
            "project_level": "Basic",
            "customer_name": "Test Tester"
        }
        self.body_add_room = {
            "name": "Room №" + self.curr_date_to_sec,
            "room_type": "Office",  # optional field to create a room
            "order": 1
            }
        self.body_edit_room = {
            "name": "Edit №" + self.curr_date_to_sec,
            "room_type": "Bathroom"
        }
        response1 = MyRequests.post("/v1/users/authenticate", data=self.payload, headers=self.x_app)
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

    @allure.description("Creating project with required fields and checking its existence")
    def test_create_and_check_project_creation(self):  # project is created only with sending required fields in JSON
        response3 = MyRequests.post("/inventory/v1/projects", data=self.body_with_required_field, headers=self.headers)
        Assertions.assert_code_status(response3, 201)
        Assertions.checking_required_field(response3, ['data', 'success'])
        Assertions.checking_required_value(response3, 'success', 'True')
        project_id = self.get_json_value(response3, 'data')['id']
        response4 = MyRequests.get(f"/inventory/v1/projects/{project_id}/project_info", headers=self.headers)
        Assertions.assert_code_status(response4, 200)
        Assertions.checking_required_field(response4, ['success', 'project'])
        Assertions.checking_required_value(response4, 'success', 'True')

    @allure.description("Creating project with required and optional fields")
    def test_create_project_with_required_optional_field(self):  # project is created with sending required and optional fields in JSON
        response5 = MyRequests.post("/inventory/v1/projects", data=self.body_with_required_optional_field,
                                    headers=self.headers)
        Assertions.assert_code_status(response5, 201)
        Assertions.checking_required_field(response5, ['data', 'success'])
        Assertions.checking_required_value(response5, 'success', 'True')
        project_id = self.get_json_value(response5, 'data')['id']
        response6 = MyRequests.get(f"/inventory/v1/projects/{project_id}/project_info", headers=self.headers)
        Assertions.assert_code_status(response6, 200)
        Assertions.checking_required_field(response6, ['success', 'project'])
        Assertions.checking_required_value(response6, 'success', 'True')

    @allure.description("Editing the details of created project")
    def test_edit_project(self):  # project is created with sending required and optional fields in JSON
        response7 = MyRequests.post("/inventory/v1/projects", data=self.body_with_required_optional_field,
                                    headers=self.headers)
        Assertions.assert_code_status(response7, 201)
        Assertions.checking_required_field(response7, ['data', 'success'])
        Assertions.checking_required_value(response7, 'success', 'True')
        project_id = self.get_json_value(response7, 'data')['id']
        response8 = MyRequests.put(f'/inventory/v1/projects/{project_id}', headers=self.headers,
                                   data={"city": "Test city",
                                         "state": "Colorado",
                                         "address": "Test Edit " + self.curr_date_to_sec,
                                         "staging_term": "12",
                                         "project_type": "Other"
                                         })
        Assertions.assert_code_status(response8, 200)
        Assertions.checking_required_field(response8, ['data', 'success'])
        Assertions.checking_required_value(response8, 'success', 'True')
        response9 = MyRequests.get(f"/inventory/v1/projects/{project_id}/project_info", headers=self.headers)  # Short project`s info
        Assertions.assert_code_status(response9, 200)
        Assertions.checking_required_field(response9, ['success', 'project'])
        Assertions.checking_required_value(response9, 'success', 'True')

    @allure.description("Add/Edit/Delete rooms in project")
    def test_with_room_to_project(self):  # project is created only with sending required fields in JSON
        response10 = MyRequests.post("/inventory/v1/projects", data=self.body_with_required_field, headers=self.headers)
        Assertions.assert_code_status(response10, 201)
        Assertions.checking_required_field(response10, ['data', 'success'])
        Assertions.checking_required_value(response10, 'success', 'True')
        project_id = self.get_json_value(response10, 'data')['id']
        response11 = MyRequests.get(f"/inventory/v1/projects/{project_id}/project_info", headers=self.headers)  # Short project`s info
        Assertions.assert_code_status(response11, 200)
        Assertions.checking_required_field(response11, ['success', 'project'])
        Assertions.checking_required_value(response11, 'success', 'True')
        response12 = MyRequests.post(f'/inventory/v1/projects/{project_id}/rooms', headers=self.headers,
                                     data=self.body_add_room)  # add new room
        Assertions.assert_code_status(response12, 201)
        Assertions.checking_required_field(response12, ['data', 'success'])
        Assertions.checking_required_value(response12, 'success', 'True')
        room_id = self.get_json_value(response12, 'data')['id']
        response13 = MyRequests.put(f"/inventory/v1/rooms/{room_id}", headers=self.headers,
                                    data=self.body_edit_room)  # edit room
        Assertions.assert_code_status(response13, 200)
        Assertions.checking_required_field(response13, ['data', 'success'])
        Assertions.checking_required_value(response13, 'success', 'True')
        response14 = MyRequests.delete(f"/inventory/v1/rooms/{room_id}", headers=self.headers)  # delete room
        Assertions.assert_code_status(response14, 200)
        Assertions.checking_required_field(response14, ['success'])
        Assertions.checking_required_value(response14, 'success', 'True')
        response15 = MyRequests.delete(f"/inventory/v1/rooms/{room_id}", headers=self.headers)  # delete room that doesn't exist
        Assertions.assert_code_status(response15, 404)
        Assertions.checking_required_field(response15, ['success', 'errors', 'data'])
        Assertions.checking_required_value(response15, 'success', 'False')
        Assertions.checking_required_value(response15, 'errors', "['Room not found']")

    @allure.description("Authorization attempt with wrong email and password")
    def test_auth_with_wrong_password(self):
        response16 = MyRequests.post("/v1/users/authenticate", headers=self.x_app,
                                     data={"email": "test3@email.com",
                                           "password": "test123"
                                           })
        Assertions.assert_code_status(response16, 401)
        Assertions.checking_required_field(response16, ['success', 'errors', 'data'])
        Assertions.checking_required_value(response16, 'success', 'False')
        Assertions.checking_required_value(response16, 'errors', "['Invalid login credentials']")

    @allure.description("Add/Edit/Delete Product")
    def test_test(self):
        pass
