from .BaseController import BaseController
from models.db_schemes import Project, DataChunk
from stores.llm.LLMEnum import DocumentTypeEnum
from typing import List
from stores.llm import LLMEnum
from langchain.prompts import ChatPromptTemplate

import json

class NLPController(BaseController):

    def __init__(self, vector_db_client, generation_client, embedding_client):
        super().__init__()
        self.vector_db_client = vector_db_client
        self.generation_client = generation_client
        self.embedding_client = embedding_client

    
    def create_collection_name(self, project_id : str):
        return f'collection_{project_id}'.strip()
    
    def reset_vector_db_collection(self, project : Project):
        collection_name = self.create_collection_name(project_id = project.project_id)
        self.vector_db_client.delete_collection(collection_name = collection_name)

    def get_vector_db_collection_info(self, project : Project):
        
        collection_name = self.create_collection_name(project_id = project.project_id)
        collection_info = self.vector_db_client.get_collection_info(collection_name = collection_name)

        return json.loads(
            json.dumps(collection_info, default=lambda x : x.__dict__)
        )

    def index_into_vector_db(self, project : Project, chunks : List[DataChunk], chunks_ids : List[int],
                                    do_reset : bool = False):
        # 1 : get collection name

        collection_name = self.create_collection_name(project_id = project.project_id)

        # 2 : manage items

        texts = [ c.chunk_text for c in chunks]
        metadata = [ c.chunk_metadata for c in chunks]

        vectors = [
            self.embedding_client.embed_text(text = text, document_type = DocumentTypeEnum.DOCUMENT.value)
            for text in texts
        ]

        # 3 : create collection if not exists
        _ = self.vector_db_client.create_collection(
            collection_name = collection_name,
            embedding_size = self.embedding_client.embedding_size,
            do_reset = do_reset

        )


        # 4 : insert into vector db
        _ = self.vector_db_client.insert_many(
            collection_name = collection_name,
            texts = texts,
            metadata = metadata,
            vectors = vectors,
            records_ids = chunks_ids
        )

        return True

    def search_vector_db_collection(self, project : Project, text : str, limit : int = 3):


        # 1 : get collection name

        collection_name = self.create_collection_name(project_id = project.project_id)

        # 2 : get text embedding vector

        vector = self.embedding_client.embed_text(
            text = text,
            document_type = DocumentTypeEnum.QUERY.value
        )

        # 3 : do semantic search

        if not vector or len(vector) == 0:
            return False

        results = self.vector_db_client.search_by_vector(collection_name = collection_name,
                                               vector = vector,
                                               limit = limit)
        

        if not results:
            return False
        
        return results
    

    def answer_rag_question(self,project : Project,  query : str, limit : int = 3):

        # 1 retrieve related document

        retrieved_document = self.search_vector_db_collection(
            project = project,
            text = query,
            limit = limit
        )

        if not retrieved_document or len(retrieved_document) == 0:
            return None, None
        

        # 2 LLM prompt

        system_prompt = """
        Answer the question based only on the following context:

        {context}

        ---

        Answer the question based on the above context: {question}

        """


        documents_prompts = "\n".join(
            system_prompt.format(context=doc.text, question=query) for idx, doc in enumerate(retrieved_document)
        )

        chat_history = [
            self.generation_client.construct_prompt(
                prompt = system_prompt,
                role = LLMEnum.OpenAIEnums.SYSTEM.value
            )
        ]

        full_prompt = "\n\n".join([documents_prompts])

        answer = self.generation_client.generate_text(
            prompt = full_prompt,
            chat_history = chat_history
        )

        return answer, full_prompt








        