## About

Сервис представляет собой обычный HTTP сервер с 2 endpoint:
1. endpoint_fast - Мгновенный возврат ответ
2. endpoint_slow - Выполнение асинхронного кода (2 запроса в MySQL)

Сервис предназначен для нагрузочного тестирования

## Start app

### Install packages
```bash
go mod download
```

### build
```bash 
go build
```

### start
```bash 
./reseatch
```