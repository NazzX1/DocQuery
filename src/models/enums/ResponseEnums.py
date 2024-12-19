from enum import Enum


class ResponseSignal(Enum):
    
    FILE_VALIDATED_SUCCESS = "file validated successfully"
    FILE_TYPE_NOT_SUPPORTED = "file type not supported"
    FILE_SIZE_EXCEEDED = "file size exceeded"
    FILE_UPLOAD_SUCCESS = "file upload succcess"
    FILE_UPLOAD_FAILED = "file upload failed"
    PROCESSING_SUCCESS = "processing success"
    PROCESSING_FAILED = "processing failed"
    NO_FILES_ERROR = "no files found"
    FILE_ID_ERROR = "no file found with this id"
    PROJECT_NOT_FOUND_ERROR = "project not found"
    INSERT_INTO_VECTORDB_ERROR = "insert into vectordb error"
    INSERT_INTO_VECTORDB_SUCCESS = "insert into vectordb success"
    VECTOR_DB_COLLECTION_RETRIEVED = "vector db collection retrieved"
    VECTORDB_SEARCH_ERROR = "vectordb search error"
    VECTORDB_SEARCH_SUCCESS = "vectordb search success"
    ANSWER_ERROR = "answer error"
    ANSWER_SUCCESS = "answer success"
