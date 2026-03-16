# AI Agent BOB Technical Specification - Part 2

## Data Schemas
### Master Dataset (501_Bottle_Dataset.csv)
Additional key fields:
- `name`: Full nomenclature.
- `spirit_type`: Categorical (Bourbon, Scotch, Japanese, etc.).
- `brand_id`: Distillery affinity.
- `proof`: Flavor intensity modeling.
- `avg_msrp`: Price-bracket alignment.
- `popularity`: Market demand score.

### User Collection Data (user_data.csv)
Fields for "distance" calculation:
- `user_id`, `product_id`, `product_name`, `brand`, `spirit`, `average_msrp`.

## API Documentation
### Marketplace Search
- **Base URL:** `https://services.baxus.co/api/search/listings`
- **Method:** `GET`
- **Params:** `q` (query), `from`, `size`, `listed` (boolean).

### User Bar Data
- **Endpoint:** `services.baxus.co/api/bar/user/{username}`
- **Method:** `GET`

## Recommendation Logic
- **Diversity Score:** Analysis of `spirit_type` and `avg_msrp` distribution.
- **Strategies:** Similarity matching (finding "close" bottles) or Strategic Diversification (introducing new regions with similar profiles).
- **Real-time Integration:** Cross-referencing recommendations with live BAXUS listings for immediate purchase links.
