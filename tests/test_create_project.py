from lib.base_case import BaseCase
from datetime import datetime

class CreateProject(BaseCase):
    def setup(self):
        base_name = "Project"
        random_name = datetime.utcnow().strftime("%M%D%Y%H%m%s") #может быть ошибка с минутами и секундами
        self.project_name = f"{base_name}{random_name}"