from langchain.schema.document import Document


def add_ids_to_chunks(chunks : list[Document]) -> list[Document]:
        """
        generate id for the chunks [id =  source : page : chunk_number]

        """

        last_page_id = None
        current_chunk_index = 0

        for chunk in chunks:
            source = chunk.metadata.get("source")
            page = chunk.metadata.get("page")

            current_page_id = f"{source}:{page}"
            
            if current_page_id == last_page_id:
                current_chunk_index += 1
            else:
                current_chunk_index = 0

            chunk_id = f"{current_page_id}:{current_chunk_index}"
            last_page_id = current_page_id
        
            chunk.metadata["id"] = chunk_id

        return chunks

