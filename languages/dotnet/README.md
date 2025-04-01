## About

Сервисы представляют собой обычный HTTP сервер с 2 endpoint:
1. endpoint_fast - Мгновенный возврат ответ
2. endpoint_slow - Выполнение асинхронного кода (2 запроса в MySQL)

Сервис предназначен для нагрузочного тестирования

## Start in Docker

### ASP.NET Core 8 в режиме Minimal API
```bash 
docker-compose -f docker-compose.dotnet.yml -p research-dotnet up -d dotnet8-minimalapi-app
```

### ASP.NET Core 8 в режиме Controllers
```bash 
docker-compose -f docker-compose.dotnet.yml -p research-dotnet up -d dotnet8-controllers-app
```

### ASP.NET Core 9 в режиме Minimal API
```bash 
docker-compose -f docker-compose.dotnet.yml -p research-dotnet up -d dotnet9-minimalapi-app
```

### ASP.NET Core 9 в режиме Controllers
```bash 
docker-compose -f docker-compose.dotnet.yml -p research-dotnet up -d dotnet9-controllers-app
```