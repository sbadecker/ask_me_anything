from typing import List, Optional

import numpy as np
import pandas as pd
import tensorflow as tf
from haystack.retriever import ElasticsearchRetriever
from transformers import AutoTokenizer, PreTrainedTokenizer, TFAutoModelForSequenceClassification


class AnaReader:
    def __init__(self, model_name: str):
        self.model = TFAutoModelForSequenceClassification.from_pretrained(
            model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.batch_size = 8

    def get_predictions(self, question: str, contexts: List[str]) -> np.array:
        X = self.get_x(question, contexts)
        dataset = self.get_inference_dataset(X, self.tokenizer)
        y_pred_logits = self.model.predict(dataset.batch(self.batch_size))[0]
        y_pred_proba = tf.math.softmax(y_pred_logits).numpy()[:, 1]
        return y_pred_proba

    def get_inference_dataset(
        self,
        X: np.array,
        tokenizer: PreTrainedTokenizer,
        truncation: bool = True,
        padding: bool = True,
        max_length: int = 256,
    ) -> tf.data.Dataset:
        encodings = tokenizer(
            list(X), truncation=truncation, padding=padding, max_length=max_length
        )
        dataset = tf.data.Dataset.from_tensor_slices((dict(encodings),))
        return dataset

    def get_x(self, question: str, contexts: List[str]) -> List[List[str]]:
        X = [[question, c] for c in contexts]
        return X


class AnaPipeline:
    def __init__(
        self, retriever: ElasticsearchRetriever, reader: AnaReader, index: str = "document"
    ):
        self.retriever = retriever
        self.reader = reader
        self.index = index

    def get_answer_documents(
        self,
        query: str,
        max_documents: Optional[int] = None,
        filters: Optional[List[str]] = None,
        threshold: float = 0.5,
        top_k: int = 250,
    ) -> pd.DataFrame:
        documents = self.retriever.retrieve(
            query, filters=filters, index=self.index, top_k=top_k)
        document_df = pd.DataFrame([d.to_dict() for d in documents])
        document_df["question"] = query
        document_df["score"] = list(
            self.reader.get_predictions(query, document_df.text.values))
        found_documents_df = document_df[document_df.score > threshold].sort_values(
            "score", ascending=False
        )
        if max_documents:
            found_documents_df = found_documents_df.iloc[:max_documents]
        return found_documents_df
