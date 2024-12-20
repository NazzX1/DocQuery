from fastapi import FastAPI, APIRouter, Depends, UploadFile, status, Request
from fastapi.responses import JSONResponse
from .schemes.nlp import PushRequest, SearchRequest
from models.enums.ResponseEnums import ResponseSignal
from models.ProjectModel import ProjectModel 
from models.ChunkModel import ChunkModel
import logging
from controllers import NLPController

logger = logging.getLogger('uvicorn.error')


npl_router = APIRouter(
    prefix = "/api/v1/nlp",
    tags = ["api_v1", "nlp"]
)

@npl_router.post("/index/push/{email}/{project_id}")
async def index_project(request : Request, project_id : str, email : str,  push_request : PushRequest):

    project_model = await ProjectModel.create_instance(
        db_client = request.app.db_client
    )

    chunk_model = await ChunkModel.create_instance(db_client = request.app.db_client)

    project = await project_model.get_project_or_create_one(
        project_id = project_id, 
        email = email 
    )

    if not project:
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = {
                "signal" : ResponseSignal.PROJECT_NOT_FOUND_ERROR.value 
            }
        )
    
    nlp_controller = NLPController(request.app.vectordb_client,
                                    request.app.generation_client,
                                      request.app.embedding_client)
    

    
    has_records = True
    page_no = 1
    inserted_items_count = 0
    idx = 0

    while has_records:
        page_chunks = await chunk_model.get_project_chunks(project_id=project.id, page=page_no)
    
        if len(page_chunks):
            page_no += 1
        
        if not page_chunks or len(page_chunks) == 0:
            has_records = False
            break

        chunks_ids =  list(range(idx, idx + len(page_chunks)))
        idx += len(page_chunks)
        
        is_inserted = nlp_controller.index_into_vector_db(
            project=project,
            chunks=page_chunks,
            do_reset=push_request.do_reset,
            chunks_ids=chunks_ids
        )

        if not is_inserted:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "signal": ResponseSignal.INSERT_INTO_VECTORDB_ERROR.value
                }
            )
        
        inserted_items_count += len(page_chunks)
        
    return JSONResponse(
        content={
            "signal": ResponseSignal.INSERT_INTO_VECTORDB_SUCCESS.value,
            "inserted_items_count": inserted_items_count
        }
    )


@npl_router.get("/index/info/{email}/{project_id}")
async def get_project_index_info(request : Request, project_id : str, email : str):
    
    project_model = await ProjectModel.create_instance(
        db_client = request.app.db_client
    )


    project = await project_model.get_project_or_create_one(
        project_id = project_id,
        email = email
    )

    nlp_controller = NLPController(request.app.vectordb_client,
                                    request.app.generation_client,
                                      request.app.embedding_client)
    
    collection_info = nlp_controller.get_vector_db_collection_info(project = project)

    return JSONResponse(
        content={
            "signal": ResponseSignal.VECTOR_DB_COLLECTION_RETRIEVED.value,
            "collection_info": collection_info
        }
    )


@npl_router.post("/index/search/{email}/{project_id}")
async def search_index(request : Request, project_id : str,email : str,  search_request : SearchRequest):
    project_model = await ProjectModel.create_instance(
        db_client = request.app.db_client
    )


    project = await project_model.get_project_or_create_one(
        project_id = project_id,
        email = email
    )

    nlp_controller = NLPController(request.app.vectordb_client,
                                    request.app.generation_client,
                                      request.app.embedding_client)
    
    results = nlp_controller.search_vector_db_collection(project = project, text = search_request.text, limit= search_request.limit)

    if not results:
        return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "signal": ResponseSignal.VECTORDB_SEARCH_ERROR.value,
        }
    )

    return JSONResponse(
        content={
            "signal": ResponseSignal.VECTORDB_SEARCH_SUCCESS.value,
            "results" : [res.dict() for res in results]
        }
    )



@npl_router.post("/index/answer/{email}/{project_id}")
async def answer_index(request : Request, project_id : str, email : str,  search_request : SearchRequest):
    project_model = await ProjectModel.create_instance(
        db_client = request.app.db_client
    )


    project = await project_model.get_project_or_create_one(
        project_id = project_id,
        email = email
    )

    nlp_controller = NLPController(request.app.vectordb_client,
                                    request.app.generation_client,
                                      request.app.embedding_client)
    

    answer, full_prompt = nlp_controller.answer_rag_question(
        project = project,
        query = search_request.text,
        limit = search_request.limit
    )

    if not answer:
        return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "signal": ResponseSignal.ANSWER_ERROR.value,
        }
    )


    return JSONResponse(
        content={
            "signal": ResponseSignal.ANSWER_SUCCESS.value,
            "anwser" : answer,
            "prompt" : full_prompt
        }
    )