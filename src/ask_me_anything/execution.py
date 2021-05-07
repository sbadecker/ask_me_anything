from haystack.document_store.elasticsearch import ElasticsearchDocumentStore
from haystack.retriever.sparse import ElasticsearchRetriever

from src.ask_me_anything.ana_pipeline.ana_pipeline import AnaReader, AnaPipeline

HOST = ""
PORT = 1234
USERNAME = ""
PASSWORD = ""
MODEL_NAME = ""


def get_answer(query, max_documents, filters=None, threshold=0.5, top_k=250):
    document_store = ElasticsearchDocumentStore(host=HOST, port=PORT, username=USERNAME, password=PASSWORD,
                                                scheme="https")
    retriever = ElasticsearchRetriever(document_store=document_store)
    reader = AnaReader(MODEL_NAME)
    ana_pipeline = AnaPipeline(retriever, reader)

    answers_df = ana_pipeline.get_answer_documents(query=query, max_documents=max_documents, filters=filters,
                                                   threshold=threshold, top_k=top_k)
    answers = answers_df.to_dict("records")
    return answers
