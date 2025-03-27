FROM python:3.11

WORKDIR /app_granian

COPY main.py .
COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 3000

CMD ["granian" ,"--interface", "asgi",  "main:app", "--port", "3000", "--host", "0.0.0.0", "--workers", "1"]
