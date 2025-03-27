FROM python:3.11

WORKDIR /app_fastapi

COPY main.py .
COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 3000

CMD ["python3", "main.py"]
