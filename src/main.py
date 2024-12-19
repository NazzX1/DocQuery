from fastapi import FastAPI
from routes import base, data, nlp
from helpers.config import Settings, get_settings
from motor.motor_asyncio import AsyncIOMotorClient
from stores.llm.LLMProviderFactory import LLMProviderFactory
from vectordb.VectorDBProviderFactory import VectorDBProviderFactory
app = FastAPI()

@app.on_event("startup")
async def startup_db_client():
    settings = get_settings()

    app.mongo_conn = AsyncIOMotorClient(settings.MONGODB_URL)
    app.db_client = app.mongo_conn[settings.MONGODB_DATABASE]

    llm_provider_factory = LLMProviderFactory(settings)
    vectordb_provider_factory = VectorDBProviderFactory(settings)

    # generation client
    app.generation_client = llm_provider_factory.create(provider = settings.GENERATION_BACKEND)
    app.generation_client.set_generation_model(settings.EMBEDDING_MODEL_ID)

    # embedding client
    app.embedding_client = llm_provider_factory.create(provider = settings.EMBEDDING_BACKEND)
    app.embedding_client.set_embedding_model(settings.EMBEDDING_MODEL_ID, settings.EMBEDDING_MODEL_size)

    # vector db client
    app.vectordb_client = vectordb_provider_factory.create(provider = settings.VECTOR_DB_BACKEND)

    app.vectordb_client.connect()



@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongo_conn.close()
    app.vectordb_client.disconnect()


app.include_router(base.base_router)
app.include_router(data.data_router)
app.include_router(nlp.npl_router)


