from flask import request

from src.app import app
from src.ask_me_anything.execution import run_answer_prediction
from src.settings import settings


@app.route("/")
@app.route("/index")
def index():
    return "Hello, World!\n"


@app.route("/get_answers", methods=["POST"])
def get_answers():
    data = request.get_json()
    answers = run_answer_prediction(query=data["text"])
    return {"answers": answers}


@app.route("/test")
def test():
    return {"summary": settings.SECRET_HEALTH_CHECK}
