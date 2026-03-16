# Project: AI Agent BOB (BAXUS)
Goal: Build a whisky expert AI agent that analyzes user collections and recommends bottles.

## Tech Stack
- Backend: Node.js / Python
- AI: OpenAI/Gemini/Claude (for whisky expertise)
- Data: Official BAXUS Hackathon Dataset (~500 bottles)
- API: `http://services.baxus.co/api/bar/user/{{username}}`

## TODO
- [x] Obtain the official dataset (TSV/CSV) - *Partial obtained*.
- [x] Create a "Whisky Knowledge Base" from the dataset.
- [x] Develop the recommendation engine logic (Flavor profile matching/Diversity).
- [x] Integrate BAXUS API structure (Search & User Bar).
- [ ] Connect Real OAuth 2.0 flow (Requires BAXUS dev access).
- [ ] Implement Full Dataset (Waiting for Carrie/Full CSV).
- [ ] Deploy as Telegram Bot or Web UI.

## Research Notes
- Discovered API endpoint: `http://services.baxus.co/api/bar/user/{{username}}`
- Identified need for flavor profile, region, and price analysis.
