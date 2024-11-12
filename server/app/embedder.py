from dotenv import load_dotenv
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain.prompts import ChatPromptTemplate
from langchain_chroma import Chroma


class EmbedderManager:
    def __init__(self) -> None:
        self.prompt_template = """
        I'm answering the question ({question}) based only on the following context:

        {context}

        ---
        """
        self.llm = self.__connectToLLM("granite3-dense", 0.8, 256)
        self.embedding_func = self.getEmbeddingFunc("granite3-dense")

    def __connectToLLM(self, model: str, temperature: float, num_predict: int):
        return ChatOllama(
            model=model,
            temperature=temperature,
            num_predict=num_predict,
        )

    def getEmbeddingFunc(self, model: str):
        return OllamaEmbeddings(model=model)

    def query(self, query_content, db: Chroma):

        results = db.similarity_search_with_score(query_content, k=5)
        
        context_text = "\n\n---\n\n".join([doc.page_content for doc, _ in results])
        
        prompt_template = ChatPromptTemplate.from_template(self.prompt_template)
        prompt = prompt_template.format(context=context_text, question=query_content)
        
        response = self.llm.invoke(prompt)
        response_text = getattr(response, "content", "").strip()

        sources = [doc.metadata.get("id", "Unknown") for doc, _ in results]
        formatted_response = f"Response:\n {response_text}\n\nSources: {sources}"

        return response_text, formatted_response