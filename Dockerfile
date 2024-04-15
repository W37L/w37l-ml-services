FROM python:3.11.7

WORKDIR /code

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

EXPOSE 80

CMD ["uvicorn", "app:init", "--host", "0.0.0.0", "--port", "80", "--proxy-headers"]