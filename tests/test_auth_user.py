import pytest

from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure


@allure.epic("Authorization cases")
class TestUserAuth(BaseCase):
    @pytest.fixture() # access the pytest library and fixture means that the setup function will be executed before our tests are run
    def setup(self):
        x_app = {"X-Application": "eames"}
        payload = {"email": "test3@email.com",
                   "password": "123123"
                   }
        response1 = MyRequests.post("/v1/users/authenticate", data=payload, headers=x_app)

        Assertions.assert_code_status(response1, 3200)
        self.token = self.get_json_value(response1, "tokens")["access_token"]
        self.client = self.get_json_value(response1, "tokens")["client"]
        self.user_id_after_auth = self.get_json_value(response1, "user")["id"]
        self.uid = self.get_header(response1, "uid")

    @allure.description("Checking user authorization with email and password")
    def test_user_auth(self, setup):

        response2 = MyRequests.get("/v1/users", headers={"client": self.client, "access_token": self.token,
                                                         "uid": self.uid, "X-Application": "eames"})
        Assertions.assert_code_status(response2, 200)
        assert "id" in response2.json()["user"], "No user_id in second response"
        user_id_with_same_uid_profile = response2.json()["user"]["id"]
        assert self.user_id_after_auth == user_id_with_same_uid_profile, f"User id: {self.user_id_after_auth} from " \
            f"first response doesn't match user id: {user_id_with_same_uid_profile} from second response"
