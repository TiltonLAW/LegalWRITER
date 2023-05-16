import os
import json
import requests

class SerpApi:
    def __init__(self):
        self.api_key = os.environ.get("58fe22a8703d6e9bcb4befc802ec3e32a28509fe4998be64138245cc7ff801f4")

    def search(self, query):
        params = {
            "engine": "google_scholar",
            "q": query,
            "api_key": self.api_key
        }
        response = requests.get("https://serpapi.com/search", params=params)
        data = json.loads(response.text)
        return data["organic_results"]
