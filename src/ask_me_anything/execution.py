from typing import List, Optional

from haystack.retriever.sparse import ElasticsearchRetriever
from src.ask_me_anything.ana_pipeline.ana_pipeline import AnaPipeline, AnaReader
from src.ask_me_anything.haystack_wrappers.haystack_elasticsearch_fix import (
    ElasticsearchDocumentStoreFixed,
)
from src.settings import settings
from src.app import ana_pipeline


def run_answer_prediction(
        query: str,
        max_documents: Optional[int] = None,
        filters: Optional[List[str]] = None,
        threshold: float = 0.5,
        top_k: int = 250,
) -> List[dict]:
    answers_df = ana_pipeline.get_answer_documents(
        query=query, max_documents=max_documents, filters=filters, threshold=threshold, top_k=top_k
    )
    answers = answers_df.to_dict("records")
    return answers
