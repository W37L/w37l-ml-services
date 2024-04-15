FROM python:3.11.7

WORKDIR /src

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

RUN mkdir -p /src
COPY src/ .

CMD ["uvicorn", "app:init", "--host", "0.0.0.0", "--port", "80"]