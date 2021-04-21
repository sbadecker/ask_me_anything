import json

import pandas as pd

BASE_DATA_DIR = "/Volumes/GoogleDrive/My Drive/Ask_me_anything/data"


def load_qa_dataset(json_path):
    qa_json = load_json(json_path)
    qa_df = pd.json_normalize(qa_json["data"],
                              record_path=["paragraphs", "qas", "answers"],
                              meta=["title",
                                    ["paragraphs", "context"],
                                    ["paragraphs", "qas", "question"],
                                    ["paragraphs", "qas", "id"],
                                    ])
    qa_df.rename(columns={
        "paragraphs.context": "context",
        "paragraphs.qas.question": "question",
        "paragraphs.qas.id": "question_id",
        "text": "answer_text"
    }, inplace=True)
    qa_df = qa_df[["title", "context", "question", "answer_text", "answer_start", "question_id"]]
    return qa_df


def load_json(path):
    with open(path, "r") as f:
        json_object = json.load(f)
    return json_object


def save_json(json_obj, path):
    with open(path, "w") as f:
        json.dump(json_obj, f)
