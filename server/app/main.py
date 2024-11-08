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

db.addChunksToDb(chunks=chunks)

