from typing import List
from qdrant_client import models, QdrantClient
from ..VectorDBInterface import VectorDBInterface
from ..VectorDBEnums import DistanceMethodsEnums
import logging
from models.db_schemes import RetrievedDocument

class QdrantDBProvider(VectorDBInterface):


    def __init__(self, url : str, api_key : str, distance_method : str):
        super().__init__()
        self.client = None
        self.url = url
        self.api_key = api_key
        self.distance_method = distance_method

        if distance_method == DistanceMethodsEnums.COSINE.value:
            self.distance_method = models.Distance.COSINE
        elif distance_method == DistanceMethodsEnums.DOT.value:
            self.distance_method = models.Distance.DOT
        

        self.logger = logging.getLogger(__name__)


    def connect(self):
        self.client = QdrantClient(url=self.url,
    api_key=self.api_key,)

    def disconnect(self):
        self.client = None

    def is_collection_existed(self, collection_name : str) -> bool:
        return self.client.collection_exists(collection_name = collection_name)


    def list_all_collections(self) -> List:
        return self.client.get_collections()
    
    def get_collection_info(self, collection_name : str):
        return self.client.get_collection(collection_name = collection_name)
    
    def delete_collection(self, collection_name : str):
        if self.is_collection_existed(collection_name = collection_name):
            return self.client.delete_collection(collection_name = collection_name)
        

    def create_collection(self, collection_name, embedding_size, do_reset = False):

        if do_reset:
            _ = self.client.delete_collection(collection_name = collection_name)
        
        if not self.is_collection_existed(collection_name = collection_name):
            _ = self.client.create_collection(
                collection_name = collection_name,
                vectors_config = models.VectorParams(
                    size = embedding_size,
                    distance = self.distance_method
                )
            )

            return True
        return False
    


    def insert_one(self, collection_name : str, text : str, vector : list,
                    metadata : dict = None,
                    record_id : str = None):
        
        if not self.is_collection_existed(collection_name = collection_name):
            return False
        
        try:   
            _ = self.client.upload_records(
                collection_name = collection_name,
                records = [
                    models.Record(
                        id = [record_id],
                        vector = vector,
                        payload = {
                            "text" : text,
                            "metadata" : metadata
                        }
                    )
                ]
            )
        except Exception as e:
            self.logger.error(f"Error occured while inserting record {e}")
            return False

        return True
    


    def insert_many(self, collection_name : str, texts : list, vectors : list,
                    metadata : list = None,
                    records_ids : list = None, batch_size : int = 50):
        if metadata is None:
            metadata = [None] * len(texts)

        if records_ids is None:
            records_ids = list(range(0, len(texts)))

        for i in range(0, len(texts), batch_size):
            batch_end = i + batch_size

            batch_texts = texts[i : batch_end]
            batch_vectors = vectors[i : batch_end]
            batch_metadata = metadata[i : batch_end]
            batch_records_ids = records_ids[i : batch_end]

            batch_records = [
                models.Record(
                    id = batch_records_ids[x],
                    vector = batch_vectors[x],
                    payload=  {
                        "text" : batch_texts[x],
                        "metadata" : batch_metadata[x]
                    }
                )
                for x in range(len(batch_texts))
            ]

            try : 
                _ = self.client.upload_records(
                collection_name = collection_name,
                records = batch_records )
            except Exception as e:
                self.logger.error(f"Error occured while inserting batch {e}")
                return False
        return True

    def search_by_vector(self, collection_name, vector : list, limit : int = 3):
        results =  self.client.search(
            collection_name = collection_name,
            query_vector = vector,
            limit = limit
        )

        if not results or len(results) == 0:
            return None

        return [
            RetrievedDocument(**{ "score" : res.score,
                                 "text" : res.payload["text"]}) 
            for res in results
        ]



