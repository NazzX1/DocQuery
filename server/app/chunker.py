from langchain_text_splitters import RecursiveCharacterTextSplitter


class ChunkerManager:
    def __init__(self, doc, chunk_size : int, overlap_size: int) -> None:        
        self.doc = doc
        self.chunk_size = chunk_size
        self.overlap_size = overlap_size
        
    def split_document(self):
        text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = self.chunk_size,
        chunk_overlap = self.overlap_size,
        length_function = len,
        is_separator_regex=False,
        )
        return text_splitter.split_documents(self.doc)
