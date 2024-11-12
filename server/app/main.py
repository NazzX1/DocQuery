from reader import ReaderManager
from chunker import ChunkerManager
from db_helper import db_helper
from embedder import EmbedderManager
import os
from dotenv import load_dotenv




_ = load_dotenv()





reader = ReaderManager("pdf","./data/Opportunités-mob-2023.pdf")

doc = reader.load()

chunker = ChunkerManager(doc, 60, 30)

chunks = chunker.split_document()


db = db_helper()

embedder = EmbedderManager()

db.connect(embedder.getEmbeddingFunc('granite3-dense'))

db.addChunksToDb(chunks=chunks)

while True :
    print('[User] : ')

    prompt = input()

    if prompt == 'quit()':
        break

    response_text, formatted_response = embedder.query(prompt, db.db)
    
    # print(response_text)
    print(formatted_response)



