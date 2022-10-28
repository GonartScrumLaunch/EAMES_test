from lib.base_case import BaseCase
from datetime import datetime
from lib.assertions import Assertions
import allure

class CreateProject(BaseCase):
    pass
    # Функция для добавления текущей даты к названия проекта
    # def setup(self):
    #     base_name = "Project"
    #     random_name = datetime.utcnow().strftime("%M%D%Y%H%m%s") #может быть ошибка с минутами и секундами
    #     self.project_name = f"{base_name}{random_name}"