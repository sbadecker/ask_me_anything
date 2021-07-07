import logging
from tempfile import NamedTemporaryFile

from flask import Flask, jsonify, request as current_request
from pydantic import ValidationError
from src.secret_manager import SecretSettings
from src.utils import get_sql_url, download_blob, get_unix_socket_sql_url
from src.settings import settings
from src.ask_me_anything.ana_pipeline.ana_pipeline import AnaPipeline, AnaReader
from werkzeug.exceptions import BadRequest, InternalServerError, NotFound, Unauthorized
from haystack.document_store.faiss import FAISSDocumentStore
from haystack.retriever import DensePassageRetriever


from src.error_handlers import (
    bad_request_400,
    internal_server_error_500,
    not_found_404,
    pydantic_validation_error_400,
    unauthorized_401,
)
from src.logger import setup_logger

logger = logging.getLogger(__name__)


def health_check():
    if current_request.args.get("noisy"):
        logger.debug("this is debug")
        logger.info("this is info")
    return jsonify({"success": True})


def add_url_rules(app):
    app.add_url_rule("/health", "health", health_check)


def register_error_handlers(app):
    app.register_error_handler(Exception, internal_server_error_500)
    app.register_error_handler(ValidationError, pydantic_validation_error_400)
    app.register_error_handler(InternalServerError, internal_server_error_500)
    app.register_error_handler(BadRequest, bad_request_400)
    app.register_error_handler(Unauthorized, unauthorized_401)
    app.register_error_handler(NotFound, not_found_404)


def make_app():
    app = Flask(__name__)

    setup_logger()
    logger.debug("loaded logger")

    logger.debug("registering endpoints...")
    add_url_rules(app)
    logger.debug("registered endpoints!")

    logger.debug("registering error handlers...")
    register_error_handlers(app)
    logger.debug("registered error handlers!")

    return app


def get_ana_pipeline(settings: SecretSettings):
    if settings.USE_UNIX_SOCKET:
        logger.info("Unix socket used")
        sql_url = get_unix_socket_sql_url()
    else:
        logger.info("Regular connection used")
        sql_url = get_sql_url()

    with NamedTemporaryFile() as f:
        download_blob(settings.DOCUMENT_EMBEDDINGS_BUCKET_NAME, source_blob_name=settings.DOCUMENT_EMBEDDINGS_FILE_NAME,
                      destination_file_name=f.name)
        faiss_document_store = FAISSDocumentStore.load(faiss_file_path=f.name, sql_url=sql_url, index="document")
    retriever = DensePassageRetriever(document_store=faiss_document_store,
                                      query_embedding_model=settings.DPR_QUERY_ENCODER_NAME,
                                      passage_embedding_model=settings.DPR_PASSAGE_ENCODER_NAME,
                                      max_seq_len_query=64,
                                      max_seq_len_passage=256,
                                      batch_size=16,
                                      use_gpu=False,
                                      embed_title=True,
                                      use_fast_tokenizers=True)
    reader = AnaReader(settings.READER_MODEL_NAME)
    ana_pipeline = AnaPipeline(retriever, reader)
    return ana_pipeline


app = make_app()

ana_pipeline = get_ana_pipeline(settings)

from src import routes

if __name__ == "__main__":
    # for debug only!!
    app.run(host="localhost", port=8000, use_reloader=True)
