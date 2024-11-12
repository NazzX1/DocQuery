from langchain_chroma import Chroma
from utils import utils
import os
from dotenv import load_dotenv
import chromadb


_ = load_dotenv()




class db_helper:
    def __init__(self) -> None:
        self.db = None

    def connect(self, embedding_function):
        self.db = Chroma(
        persist_directory="./chroma_db", embedding_function=embedding_function
        )
        print('[INFO] connected to db')

    def addChunksToDb(self, chunks):
        chunks_with_ids = utils.add_ids_to_chunks(chunks)
        # Add or Update the documents.
        existing_items = self.db.get(include=[])  # IDs are always included by default
        existing_ids = set(existing_items["ids"])
        print(f"Number of existing documents in DB: {len(existing_ids)}")

        # Only add documents that don't exist in the DB.
        new_chunks = []
        print(chunks_with_ids[0])
        for chunk in chunks_with_ids:
            if chunk.metadata["id"] not in existing_ids:
                new_chunks.append(chunk)

        if len(new_chunks):
            print(f"👉 Adding new documents: {len(new_chunks)}")
            new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
            self.db.add_documents(documents = chunks_with_ids, ids=new_chunk_ids)
            print("documents been loading succesfully")
        else:
            print("✅ No new documents to add")





    