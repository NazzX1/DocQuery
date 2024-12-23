from helpers.config import Settings, get_settings
import os
import random
import string

class BaseController:


    def __init__(self):
        self.app_settings = get_settings()
        self.base_dir = os.path.dirname(os.path.dirname(__file__))
        self.file_dir = os.path.join(
            self.base_dir,
            "assets/files"
        )


    def generate_random_string(self, length : int = 12):
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k = length))
    
    def get_database8URL(self):

        return self.app_settings.VECTOR_DB_URL

    def get_database8URL(self):

        return self.app_settings.VECTOR_DB_API_KEY
