from typing import List, Optional

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
