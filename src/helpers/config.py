from pydantic_settings import BaseSettings, SettingsConfigDict



class Settings(BaseSettings):

    APP_NAME : str
    APP_VERSION : str

    FILE_ALLOWED_EXTENSIONS : list
    FILE_MAX_SIZE : int
    FILE_DEFAULT_CHUNK_SIZE : int

    MONGODB_URL : str
    MONGODB_DATABASE : str


    GENERATION_BACKEND : str
    EMBEDDING_BACKEND : str


    OPENAI_API_KEY : str = None 
    OPENAI_API_URL : str = None

    GENERATION_MODEL_ID : str = None
    EMBEDDING_MODEL_ID : str = None
    EMBEDDING_MODEL_size : str = None

    INPUT_DEFAULT_MAX_CHARACHTERS : int = None
    GENERATION_DEFAULT_MAX_TOKENS : int = None
    GENERATION_DEFAULT_TEMPERATURE : float = None


    VECTOR_DB_BACKEND : str
    VECTOR_DB_URL : str
    VECTOR_DB_API_KEY : str
    VECTOR_DB_DISTANCE_METHOD : str = None

    class Config:
        env_file = ".env"

    
def get_settings():
    return Settings()