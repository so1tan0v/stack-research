# locust -f locust.py --master --expect-workers 8
# locust -f locust.py --worker --master-host=127.0.0.1 &

import time
from locust import HttpUser, task, between

class WebsiteUserTest(HttpUser):
    host = "http://localhost:3000"

    @task
    def fast_page(self):
        self.client.get(url="/endpoint_fast")

    # @task
    # def slow_page(self):
    #     self.client.get(url="/endpoint_slow")