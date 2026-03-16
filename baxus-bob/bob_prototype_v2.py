import csv
import math

class BobWhiskyAgent:
    def __init__(self, dataset_path):
        self.data = []
        try:
            with open(dataset_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f, delimiter='\t')
                for row in reader:
                    row['proof'] = float(row['proof']) if row['proof'] else 0.0
                    row['abv'] = float(row['abv']) if row['abv'] else 0.0
                    row['avg_msrp'] = float(row['avg_msrp']) if row['avg_msrp'] else 0.0
                    row['id'] = int(row['id'])
                    self.data.append(row)
        except Exception as e:
            print(f"Error loading dataset: {e}")

    def cosine_similarity(self, v1, v2):
        dot_product = sum(a * b for a, b in zip(v1, v2))
        magnitude1 = math.sqrt(sum(a**2 for a in v1))
        magnitude2 = math.sqrt(sum(b**2 for b in v2))
        if magnitude1 == 0 or magnitude2 == 0: return 0
        return dot_product / (magnitude1 * magnitude2)

    def get_diversity_score(self, user_bar_ids):
        """Calculates diversity based on spirit types owned."""
        user_bottles = [b for b in self.data if b['id'] in user_bar_ids]
        if not user_bottles: return 0
        
        types = [b['spirit_type'] for b in user_bottles]
        unique_types = set(types)
        # Entropy-lite: ratio of unique types to total bottles
        return len(unique_types) / len(types)

    def get_recommendations(self, user_bar_ids, n=3, strategy="balanced"):
        user_bottles = [b for b in self.data if b['id'] in user_bar_ids]
        if not user_bottles: return []

        # Get unique types owned to handle diversity
        owned_types = set(b['spirit_type'] for b in user_bottles)
        
        candidates = []
        for candidate in self.data:
            if candidate['id'] in user_bar_ids: continue
            
            # Feature Vector: [Proof, ABV, Price]
            cand_vec = [candidate['proof'], candidate['abv'], candidate['avg_msrp']]
            
            similarities = []
            for user_bottle in user_bottles:
                user_vec = [user_bottle['proof'], user_bottle['abv'], user_bottle['avg_msrp']]
                similarities.append(self.cosine_similarity(cand_vec, user_vec))
            
            avg_sim = sum(similarities) / len(similarities)
            
            # Diversity adjustment
            diversity_boost = 0
            if strategy == "diverse" and candidate['spirit_type'] not in owned_types:
                diversity_boost = 0.2 # Boost bottles from new categories
            
            final_score = avg_sim + diversity_boost
            candidates.append((candidate, final_score, avg_sim))

        candidates.sort(key=lambda x: x[1], reverse=True)
        return candidates[:n]

if __name__ == "__main__":
    agent = BobWhiskyAgent('baxus-bob/dataset_sample.tsv')
    # User owns only Bourbons (Blanton's and Eagle Rare)
    user_bar = [164, 2848] 
    
    print(f"--- BOB Advanced Prototype ---")
    div_score = agent.get_diversity_score(user_bar)
    print(f"Current Bar Diversity Score: {div_score:.2f} (Low diversity detected)\n")
    
    print("Strategy: Balanced (Finding similar favorites)")
    recs = agent.get_recommendations(user_bar, strategy="balanced")
    for i, (rec, score, sim) in enumerate(recs):
        print(f"{i+1}. {rec['name']} - {rec['spirit_type']} (Similarity: {sim:.2f})")

    print("\nStrategy: Diverse (Expanding horizons)")
    # Note: Our sample dataset is mostly Bourbon, but let's see if it finds the 'Rye' entry
    recs_div = agent.get_recommendations(user_bar, strategy="diverse")
    for i, (rec, score, sim) in enumerate(recs_div):
        is_new = "NEW CATEGORY!" if rec['spirit_type'] not in ["Bourbon"] else ""
        print(f"{i+1}. {rec['name']} - {rec['spirit_type']} {is_new} (Score: {score:.2f})")
