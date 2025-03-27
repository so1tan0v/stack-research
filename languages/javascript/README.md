## About

Сервисы представляют собой обычный HTTP сервер с 2 endpoint:
1. endpoint_fast - Мгновенный возврат ответ
2. endpoint_slow - Выполнение асинхронного кода (2 запроса в MySQL)

Сервис предназначен для нагрузочного тестирования

## Start in Docker

### Vanila
```bash 
docker-compose -f docker-compose.javascript.yml -p research-javascript up -d nodejs-vanila-app
```

### Express
```bash 
docker-compose -f docker-compose.javascript.yml -p research-javascript up -d nodejs-express-app
```

### Fastify
```bash 
docker-compose -f docker-compose.javascript.yml -p research-javascript up -d nodejs-fastify-app
```

### Bun. Vanila
```bash 
docker-compose -f docker-compose.javascript.yml -p research-javascript up -d bun-vanila-app
```

### Bun. Fastify
```bash 
docker-compose -f docker-compose.javascript.yml -p research-javascript up -d bun-fastify-app
```

## Native start app 

### Install packages
```bash
npm install
```

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

### Bun. Vanila
```bash 
bun run vanila.js
```

### Bun. Fastify
```bash 
bun run fastify.js
```