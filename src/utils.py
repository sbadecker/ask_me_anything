import json

import pandas as pd

BASE_DATA_DIR = "/Volumes/GoogleDrive/My Drive/Ask_me_anything/data"


def load_german_quad_dataset(json_path):
    dummy_dict = {key: None for key in ["answer_id", "document_id", "question_id", "text",
                                        "answer_start", "answer_category"]}
    qa_json = load_json(json_path)
    qa_df = pd.json_normalize(qa_json["data"],
                              record_path=["paragraphs", "qas"],
                              meta=[
                                  ["paragraphs", "context"],
                                  ["paragraphs", "document_id"]
                              ])
    qa_df["answers"] = qa_df.answers.map(lambda x: x if len(x) != 0 else dummy_dict)
    answers_df = pd.concat(qa_df.answers.map(pd.json_normalize).values).reset_index(drop=True)
    
    qa_df = pd.concat([qa_df, answers_df], axis=1)
    
    qa_df.drop(columns=["answers", "question_id", "document_id"], inplace=True)
    qa_df.rename(columns={
        "paragraphs.context": "context",
        "paragraphs.document_id": "document_id",
        "text": "answer_text",
        "id": "question_id"
    }, inplace=True)
    return qa_df


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


def convert_drp_to_ana(json_path):
    dpr_json = load_json(json_path)
    meta_columns = ["question", "answers"]
    negatives_df = pd.json_normalize(dpr_json,
                                     record_path=["hard_negative_ctxs"],
                                     meta=meta_columns
                                    )
    positives_df = pd.json_normalize(dpr_json,
                                     record_path=["positive_ctxs"],
                                     meta=meta_columns
                                    )
    negatives_df["contains_answer"] = False
    positives_df["contains_answer"] = True
    
    ana_df = pd.concat([negatives_df, positives_df]).reset_index(drop=True)
    ana_df.rename(columns={"text": "context", "answers": "answer"}, inplace=True)
    return ana_df


def load_json(path):
    with open(path, "r") as f:
        json_object = json.load(f)
    return json_object


def save_json(json_obj, path):
    with open(path, "w") as f:
        json.dump(json_obj, f)
