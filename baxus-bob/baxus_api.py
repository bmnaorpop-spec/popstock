import requests
import json
import os

class BaxusAPIClient:
    def __init__(self, base_url="https://services.baxus.co/api"):
        self.base_url = base_url

    def get_user_bar(self, username):
        """Fetches the virtual bar for a given BAXUS username."""
        url = f"{self.base_url}/bar/user/{username}"
        try:
            print(f"Fetching bar for user: {username}...")
            # Note: In production, this would need OAuth headers
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error: Received status code {response.status_code}")
                return None
        except Exception as e:
            print(f"Request failed: {e}")
            return None

    def search_listings(self, query, listed=True):
        """Searches for live listings on the BAXUS marketplace."""
        url = f"{self.base_url}/search/listings"
        params = {
            "q": query,
            "listed": str(listed).lower(),
            "size": 5
        }
        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Search failed: {e}")
            return None

if __name__ == "__main__":
    client = BaxusAPIClient()
    # Test with a placeholder/hypothetical user to see if endpoint is live
    # We don't have a real username yet, so we just prepare the structure
    print("API Client initialized. Ready to connect to BAXUS infrastructure.")
