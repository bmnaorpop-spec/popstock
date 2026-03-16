# AI Agent BOB Technical Specification - Part 1

## Overview
Bob is an autonomous whiskey sommelier designed for the BAXUS ecosystem. 

## Operational Modules
1. **Collection Analysis:** Identifies patterns (peat levels, age, price) from user bar data.
2. **Recommendation Engine:** Maps similarities and aligns with market pricing using the master dataset.
3. **Ranking Framework:** Scores relevance and generates natural language reasoning.
4. **Output Interface:** Provides narrative explanations and visualizations.

## Data Schema (Partial)
- **Dataset:** `501_Bottle_Dataset.csv` (approx. 501 bottles).
- **Mandatory Fields:** `id` (Integer), `name`, `size`, `proof`, `abv`, `spirit_type`, `brand_id`, `popularity`, `avg_msrp`, `fair_price`, `shelf_price`, `total_score`, `wishlist_count`, `vote_count`, `bar_count`, `ranking`.

## Key Logic
- Semantic analysis of flavor profiles.
- Diversification vs. Reinforcement strategies.
