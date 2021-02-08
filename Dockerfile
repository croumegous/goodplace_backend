FROM python:3.8.6-slim-buster

RUN apt-get update && apt-get install -y gcc libpq-dev&& \
    pip install "poetry==1.1.4"
    
WORKDIR /src

ENV PYTHONUNBUFFERED 1

COPY poetry.lock pyproject.toml /src/

RUN poetry config virtualenvs.create false \
  && poetry install

COPY . /src

EXPOSE 80

CMD ["uvicorn", "good_place.main:app", "--host", "0.0.0.0", "--port", "80"]
