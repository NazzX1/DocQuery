from .BaseController import BaseController
from fastapi import UploadFile
from .ProjectController import ProjectController
from models import ResponseSignal
import os
import re


class DataController(BaseController):
    
    def __init__(self):
        super().__init__()
        self.size_scale = 1048576 # convert MB to Bytes



    def validate_uploaded_file(self, file : UploadFile):
        
        if file.content_type not in self.app_settings.FILE_ALLOWED_EXTENSIONS:
            return False, ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value

        if file.size > self.app_settings.FILE_MAX_SIZE * self.size_scale:
            return False, ResponseSignal.FILE_SIZE_EXCEEDED.value
        
        return True, ResponseSignal.FILE_VALIDATED_SUCCESS.value
    
    def generate_unique_filename(self, orig_filename : str,  project_id : str):
        
        random_key = self.generate_random_string()
        project_path = ProjectController().get_project_path(project_id=project_id)

        cleaned_filename = self.get_clean_filename(
            orig_filename = orig_filename
        )

        new_file_path = os.path.join(
            project_path,
            random_key + "_" + cleaned_filename
        )


        while os.path.exists(new_file_path):
            random_key = self.generate_random_string()
            new_file_path = os.path.join(
                project_path,
                random_key + '_' + cleaned_filename
            )

        return new_file_path, random_key + '_' + cleaned_filename

    def get_clean_filename(self, orig_filename : str):

        cleaned_file_name = re.sub(r'[^\w.]', "", orig_filename.strip())

        cleaned_file_name = cleaned_file_name.replace(" ", "_")

        return cleaned_file_name


