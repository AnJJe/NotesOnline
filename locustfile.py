from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(0.5, 15)
    @task(1)
    def index(self):
        self.client.get("/")