FROM python:3.13

WORKDIR /app_granian

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY main.py .

EXPOSE 3000

CMD ["python" , "main.py"]
