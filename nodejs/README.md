## About

Сервисы представляют собой обычный HTTP сервер с 2 endpoint:
1. endpoint_fast - Мгновенный возврат ответ
2. endpoint_slow - Выполнение асинхронного кода (2 запроса в MySQL)

Сервис предназначен для нагрузочного тестирования

## Start app

### Vanila
```bash 
node vanila.js
```

### Express
```bash 
node express.js
```

### Fastify
```bash 
node fastify.js
```