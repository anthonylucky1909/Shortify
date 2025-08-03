from locust import HttpUser, task, between
import random

# Simulate backend servers on different ports
ports = [8000, 8001, 8002]

# Minimal URL pool to hammer deduplication/cache layer
long_urls = ["https://a.com", "https://b.com", "https://c.com"]

# Shared (non-thread-safe) list for speed testing
short_ids = []

class MultiServerUser(HttpUser):
    wait_time = between(0, 0)  # No delay between requests
    host = "http://localhost"  # Required by Locust, not used directly

    def choose_base_url(self):
        return f"http://localhost:{random.choice(ports)}"

    @task(2)
    def write_url(self):
        base_url = self.choose_base_url()
        long_url = random.choice(long_urls)
        with self.client.post(f"{base_url}/shorten", json={"long_url": long_url}, catch_response=True) as response:
            if response.status_code == 200:
                try:
                    short_id = response.json().get("short_id")
                    if short_id:
                        short_ids.append(short_id)  # No locking for speed
                except Exception as e:
                    response.failure(f"Error parsing JSON: {e}")
            else:
                response.failure("Failed to shorten URL")

    @task(5)
    def read_url(self):
        if short_ids:
            short_id = random.choice(short_ids)
            base_url = self.choose_base_url()
            self.client.get(f"{base_url}/{short_id}")

    @task(1)
    def analytics(self):
        if short_ids:
            short_id = random.choice(short_ids)
            base_url = self.choose_base_url()
            self.client.get(f"{base_url}/analytics/{short_id}")
