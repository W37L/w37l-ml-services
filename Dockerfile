FROM python:3.11.7

WORKDIR /src

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt
RUN pip install uvicorn

RUN mkdir -p /src
COPY src/ /src/

CMD ["uvicorn", "src.mlservice.app:app", "--host", "0.0.0.0", "--port", "80"]