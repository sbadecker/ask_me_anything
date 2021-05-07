import pandas as pd
import tensorflow as tf
from tensorflow.data import Dataset
from transformers import TFAutoModelForSequenceClassification, AutoTokenizer


class AnaPipeline:
    def __init__(self, retriever, reader, index="document"):
        self.retriever = retriever
        self.reader = reader
        self.index = index

    def get_answer_documents(self, query, max_documents, filters=None, threshold=0.5, top_k=250):
        documents = self.retriever.retrieve(query, filters=filters, index=self.index, top_k=top_k)
        document_df = pd.DataFrame([d.to_dict() for d in documents])
        document_df["question"] = query
        document_df["score"] = list(self.reader.get_predictions(query, document_df.text.values))
        found_documents_df = document_df[document_df.score > threshold].sort_values("score",
                                                                                    ascending=False)[:max_documents]
        return found_documents_df


class AnaReader:
    def __init__(self, model_name):
        self.model = TFAutoModelForSequenceClassification.from_pretrained(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.batch_size = 8

    def get_predictions(self, question, contexts):
        X = self.get_x(question, contexts)
        dataset = self.get_inference_dataset(X, self.tokenizer)
        y_pred_logits = self.model.predict(dataset.batch(self.batch_size))[0]
        y_pred_proba = tf.math.softmax(y_pred_logits).numpy()[:, 1]
        return y_pred_proba

    def get_inference_dataset(self, X, tokenizer, truncation=True, padding=True, max_length=256):
        encodings = tokenizer(
            list(X),
            truncation=truncation,
            padding=padding,
            max_length=max_length
        )
        dataset = Dataset.from_tensor_slices((
            dict(encodings),
        ))
        return dataset

    def get_x(self, question, contexts):
        X = [[question, c] for c in contexts]
        return X
