from bob_prototype_v2 import BobWhiskyAgent
from baxus_api import BaxusAPIClient
import time

def main():
    print("--- BOB: BAXUS Onchain Butler (v1.0-alpha) ---")
    
    # 1. Initialize Components
    agent = BobWhiskyAgent('baxus-bob/dataset_sample.tsv')
    api = BaxusAPIClient()
    
    # 2. Setup (Manual for now, will be username-based)
    username = "test_user" 
    print(f"Targeting user: {username}")
    
    # 3. Analyze Bar (Simulation + API preparation)
    # Since we don't have a real username yet, we use our prototype user bar
    user_bar_ids = [164, 2848] 
    
    print("\n[BOB] Step 1: Analyzing your Virtual Bar...")
    div_score = agent.get_diversity_score(user_bar_ids)
    print(f"[BOB] Your Diversity Score is {div_score:.2f}.")
    
    # 4. Generate Recommendations
    print("\n[BOB] Step 2: Selecting the perfect bottles for you...")
    strategy = "diverse" if div_score < 0.6 else "balanced"
    recommendations = agent.get_recommendations(user_bar_ids, n=2, strategy=strategy)
    
    # 5. Live Market Integration (The "Real" Bob)
    print("\n[BOB] Step 3: Checking live BAXUS availability...")
    for bottle, score, sim in recommendations:
        print(f"\nRecommended: {bottle['name']}")
        print(f"Reasoning: {bottle['spirit_type']} matching your current profile but expanding your collection.")
        
        # Call the live API to see if it's for sale
        listings = api.search_listings(bottle['name'])
        if listings and len(listings) > 0:
            print(f"✅ LIVE DEAL FOUND! Price: {listings[0].get('price', 'Check Site')}")
            print(f"🔗 Link: https://www.baxus.co/listings/{listings[0].get('id', '')}")
        else:
            print("❌ Not currently listed in the BAXUS vault. Added to your automated wishlist.")

if __name__ == "__main__":
    main()
