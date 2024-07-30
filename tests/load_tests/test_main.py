from locust import HttpUser, TaskSet, task


# class LotBehavior(TaskSet):
#     # @task(1)
#     # def index(self):
#     #     self.client.get("/api/v1/lots/all")


class UserBehavior(TaskSet):
    # @task(5)
    # def list_users(self):
    #     self.client.get("/api/v1/users/all")

    @task(1)
    def create_user(self):
        self.client.post(
            "/api/v1/users",
            {"username": "xxxasdsd", "hashed_password": "xxxxxxxxxxxx", "balance": 0},
        )


class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    min_wait = 1000
    max_wait = 2000
