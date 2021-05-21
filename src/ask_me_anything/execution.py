from typing import List, Optional
from haystack.retriever.sparse import ElasticsearchRetriever

from src.ask_me_anything.ana_pipeline.ana_pipeline import AnaPipeline, AnaReader
from src.ask_me_anything.haystack_wrappers.haystack_elasticsearch_fix import (
    ElasticsearchDocumentStoreFixed,
)
from src.settings import settings


def run_answer_prediction(
    query: str,
    max_documents: Optional[int] = None,
    filters: Optional[List[str]] = None,
    threshold: float = 0.5,
    top_k: int = 250,
) -> List[dict]:
    document_store = ElasticsearchDocumentStoreFixed(
        host=settings.ELASTICSEARCH_HOST,
        port=settings.ELASTICSEARCH_PORT,
        username=settings.ELASTICSEARCH_USERNAME,
        password=settings.ELASTICSEARCH_PASSWORD,
        scheme="https",
    )
    retriever = ElasticsearchRetriever(document_store=document_store)
    reader = AnaReader(settings.READER_MODEL_NAME)
    ana_pipeline = AnaPipeline(retriever, reader)

    answers_df = ana_pipeline.get_answer_documents(
        query=query, max_documents=max_documents, filters=filters, threshold=threshold, top_k=top_k
    )
    answers = answers_df.to_dict("records")
    return answers
