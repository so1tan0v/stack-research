## About

Сервисы представляют собой обычный HTTP сервер с 2 endpoint:
1. endpoint_fast - Мгновенный возврат ответ
2. endpoint_slow - Выполнение асинхронного кода (2 запроса в MySQL)

Сервис предназначен для нагрузочного тестирования

## Start app

### Install packages

```bash
pip install -r requirements.txt
```

### Start

#### Granian
```bash 
cd granian; granian --interface asgi main:app --port 3000 --workers 1
```

#### FastAPI
```bash 
python fastapi/main.py
```