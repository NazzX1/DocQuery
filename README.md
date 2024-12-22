<h1 align='center'>DocQuery</h1>

This project leverages AI to efficiently search, retrieve, and answer questions from documents. It processes text chunks, embeds them for similarity search, and provides contextual responses based on the user's query.

## Technologies Used
- **Python**
- **LangChain**
- **Qdrant**
- **Ollama**


## How to Run
1. Clone the repository.
2. Install the required dependencies:
    ```
    pip install -r requirements.txt
    ```
3. Set up environment variables :
    ```bash
    $ cp .env.example .env
    ```
5. Run the FastApi server:
    ```
    uvicorn main:app
    ```
