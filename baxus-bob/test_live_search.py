import requests

def test_baxus_search(query):
    print(f"--- BOB Live Search Test ---")
    print(f"Searching for: {query}\n")
    
    url = "https://services.baxus.co/api/search/listings"
    params = {
        "q": query,
        "listed": "true",
        "size": 5
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            results = response.json()
            if not results:
                print("No live listings found for this exact query.")
                return
            
            print(f"Found {len(results)} active listings:\n")
            for i, item in enumerate(results):
                # Using .get() because we aren't 100% sure of the field names yet
                name = item.get('name', item.get('product_name', 'Unknown'))
                price = item.get('price', 'Price not listed')
                listing_id = item.get('id', '')
                print(f"{i+1}. {name}")
                print(f"   Price: {price}")
                print(f"   Link: https://www.baxus.co/listings/{listing_id}\n")
        else:
            print(f"API Error: {response.text}")
            
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    test_baxus_search("Pappy Van Winkle 20 Year Family Reserve 2021")
