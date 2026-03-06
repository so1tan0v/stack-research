.PHONY: start-locust stop-locust start-mysql stop-mysql start-javascript-apps stop-javascript-apps start-python-apps stop-python-apps start-golang-apps stop-golang-apps start-dotnet-apps stop-dotnet-apps

# Tests
start-locust:
	docker compose -f docker-compose.locust.yml -p research-test-locust up -d
stop-locust:
	docker compose -f docker-compose.locust.yml -p research-test-locust up -d

# Infrastructure
start-mysql:
	docker compose -f docker-compose.mysql.yml up -d

# Applications
## Start
start-javascript-apps:
	docker compose -f docker-compose.javascript.yml -p research-javascript up -d
start-python-apps:
	docker compose -f docker-compose.python.yml -p research-python up -d
start-golang-apps:
	docker compose -f docker-compose.golang.yml -p research-golang up -d
start-dotnet-apps:
	docker compose -f docker-compose.dotnet.yml -p research-dotnet up -d

## Stop
stop-javascript-apps:
	docker compose -p research-javascript down
stop-python-apps:
	docker compose -p research-python down
stop-golang-apps:
	docker compose -p research-golang down
stop-dotnet-apps:
	docker compose -p research-dotnet down



help:
	@echo "Usage: make <target>"
	@echo "Targets:"
	@echo "  start-locust - Start Locust"
	@echo "  stop-locust - Stop Locust"
	@echo "  start-mysql - Start MySQL"
	@echo "  stop-mysql - Stop MySQL"
	@echo "  start-javascript-apps - Start Node.js apps"
	@echo "  stop-javascript-apps - Stop Node.js apps"
	@echo "  start-python-apps - Start Python apps"
	@echo "  stop-python-apps - Stop Python apps"
	@echo "  start-golang-apps - Start Go apps"
	@echo "  stop-golang-apps - Stop Go apps"
	@echo "  start-dotnet-apps - Start ASP.NET Core apps"
	@echo "  stop-dotnet-apps - Stop ASP.NET Core apps"