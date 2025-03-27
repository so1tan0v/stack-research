# Tests
start-locust:
	docker-compose -f docker-compose.locust.yml -p research-test-locust up -d
stop-locust:
	docker-compose -f docker-compose.locust.yml -p research-test-locust up -d

# Applications
## Start
start-javascript-apps:
	docker-compose -f docker-compose.javascript.yml -p research-javascript up -d
start-python-apps:
	docker-compose -f docker-compose.python.yml -p research-python up -d
start-golang-apps:
	docker-compose -f docker-compose.golang.yml -p research-golang up -d

## Stop
stop-javascript-apps:
	docker-compose -p research-javascript down
stop-python-apps:
	docker-compose -p research-python down
stop-golang-apps:
	docker-compose -p research-golang down

