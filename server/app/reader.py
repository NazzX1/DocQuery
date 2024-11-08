from langchain_community.document_loaders import PyPDFLoader
import os

class ReaderManager:
    def __init__(self, file_type, path) -> None:
        self.file_type = file_type
        self.path = path

    def load(self):
        try:
            loader= PyPDFLoader(self.path)
            return loader.load()
        except Exception as e:
            print(f'Failed to Load the doc : {e}')







        