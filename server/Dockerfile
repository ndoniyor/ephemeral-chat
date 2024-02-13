FROM python:3.9-slim

WORKDIR /app

ADD . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 11912

CMD ["python", "serve.py"]