import csv
import math

class BobWhiskyAgent:
    def __init__(self, dataset_path):
        self.data = []
        with open(dataset_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter='\t')
            for row in reader:
                # Convert strings to floats for math
                row['proof'] = float(row['proof']) if row['proof'] else 0.0
                row['abv'] = float(row['abv']) if row['abv'] else 0.0
                row['avg_msrp'] = float(row['avg_msrp']) if row['avg_msrp'] else 0.0
                row['id'] = int(row['id'])
                self.data.append(row)

    def cosine_similarity(self, v1, v2):
        "Math: (A . B) / (||A|| * ||B||)"
        dot_product = sum(a * b for a, b in zip(v1, v2))
        magnitude1 = math.sqrt(sum(a**2 for a in v1))
        magnitude2 = math.sqrt(sum(b**2 for b in v2))
        if magnitude1 == 0 or magnitude2 == 0: return 0
        return dot_product / (magnitude1 * magnitude2)

    def get_recommendations(self, user_bar_ids, n=3):
        user_bottles = [b for b in self.data if b['id'] in user_bar_ids]
        if not user_bottles:
            return "Your bar is empty!"

        recommendations = []
        for candidate in self.data:
            if candidate['id'] in user_bar_ids: continue
            
            # Feature Vector: [Proof, ABV, Price]
            cand_vec = [candidate['proof'], candidate['abv'], candidate['avg_msrp']]
            
            # Average similarity to everything in user's bar
            similarities = []
            for user_bottle in user_bottles:
                user_vec = [user_bottle['proof'], user_bottle['abv'], user_bottle['avg_msrp']]
                similarities.append(self.cosine_similarity(cand_vec, user_vec))
            
            avg_sim = sum(similarities) / len(similarities)
            recommendations.append((candidate, avg_sim))

        # Sort by similarity score
        recommendations.sort(key=lambda x: x[1], reverse=True)
        return recommendations[:n]

# --- Prototype Test ---
if __name__ == "__main__":
    agent = BobWhiskyAgent('baxus-bob/dataset_sample.tsv')
    user_bar = [164, 2848] # Blanton's and Eagle Rare
    
    print(f"--- BOB Prototype Analysis (No-Dependency Version) ---")
    print(f"User owns: Blanton's Original, Eagle Rare\n")
    
    recs = agent.get_recommendations(user_bar)
    for i, (rec, score) in enumerate(recs):
        print(f"{i+1}. {rec['name']} (Match: {score:.2f})")
        print(f"   Type: {rec['spirit_type']}, Price: ${rec['avg_msrp']}")
        print(f"   BOB says: \"If you liked the intensity of your current collection, you'll love this {rec['spirit_type']}.\"\n")
