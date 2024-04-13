FROM python:3.11.7

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

RUN mkdir -p /src
COPY src/ /src/

WORKDIR /src

RUN pip install -e .

COPY tests/ /tests/

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]