FROM python:3.7

ENV PYTHONUNBUFFERED True

RUN pip install poetry

COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction

COPY src/ src/
COPY models/ models/
ENV PORT 5000
EXPOSE $PORT

CMD exec gunicorn --bind :$PORT src.app:app --workers 1 --threads 1 --timeout 0