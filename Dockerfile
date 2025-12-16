FROM python:3.12-slim

RUN pip install --upgrade pip && pip install poetry

WORKDIR /finmindai

COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --only main --no-root

COPY . .

EXPOSE 8081

CMD ["python", "-m", "application.main"]


