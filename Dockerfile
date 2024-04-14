FROM python:3.11.7

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt
RUN pip install uvicorn

RUN mkdir -p /src
COPY src/ /src/

WORKDIR /src
CMD ["python", "src/mlearning/app.py"]