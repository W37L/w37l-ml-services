FROM python:3.11.7

# RUN apt install gcc libpq (no longer needed bc we use psycopg2-binary)

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

RUN mkdir -p /mlservice
COPY mlservice/ /src/
RUN pip install -e /mlservice
COPY tests/ /tests/

WORKDIR /mlservice
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]