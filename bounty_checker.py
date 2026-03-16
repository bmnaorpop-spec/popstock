#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import os
import json

def check_bounties():
    url = "https://superteam.fun/earn" # Simplified entry
    try:
        response = requests.get(url, timeout=15)
        # In a real scenario, we might need a more robust scraper if it's SSR/Hydrated
        # But let's assume we can find listings in the HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # This is a placeholder for actual parsing logic
        # For now, we search for common bounty keywords and small amounts
        listings = []
        for item in soup.find_all(string=True):
            if "$" in item and ("USDC" in item or "SOL" in item):
                # Basic heuristic: look for amounts between 100 and 1000
                parent = item.parent
                text = parent.get_text()
                listings.append(text)
        
        return listings
    except Exception as e:
        return [f"Error: {str(e)}"]

if __name__ == "__main__":
    results = check_bounties()
    # Logic to filter and notify would go here
    print(json.dumps(results[:5]))
