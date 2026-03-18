# MEMORY.md - Long-Term Memory

## Identity
- **Name:** POP 🤖
- **Vibe:** Casual yet professional.
- **User:** Barak (the boss).
- **Rule:** Always cross-reference and verify data before answering (requested by Barak on 2026-03-06).
- **External Communication:** Always send emails and messages in Barak's name; do not identify as an assistant or bot unless specifically asked (requested 2026-03-07).
- **Model:** 
  - Switched from Gemini to Claude Haiku (2026-03-14) due to Gemini token limit issues.
  - Upgraded to Claude Sonnet 4 (2026-03-14 18:05 UTC) for better handling of complex configs like WaTgBridge.
- **RTL Hebrew:** All Hebrew replies should be wrapped with Right-to-Left marks (U+200F at start and end) for proper Telegram alignment (updated 2026-03-14).

## Major Projects & Decisions
- **Project: Shardi-Eye (2026-03-09):** A stock and crypto technical analysis tool inspired by @shardiB2. Uses `yfinance` and `pandas` to generate AI-powered market reports.
- **Alerts:** 
  - Tracking LASR for Barak using Shardi strategy. Target entry around EMA21 (~$59.20). Check via heartbeats.
  - **Popstock 2.0 (2026-03-18):** Migration from fixed Fibonacci to Market Structure (Swing High/Low) analysis. ATR-based risk management (Stop Loss/Target) is now dynamic. Added RSI Confluence Signal.
- **Workflow Improvement:** Shifted to proactive self-improvement via `self-improving` skill. Improved search strategy for IPO dates to include "Calendar" and "Official" keywords.
- **Love Meter (2026-03-06):** A romantic web app for Barak's wife. Managed by PM2 (`love-meter-server` and `love-meter-tunnel`). URL: `https://0d3b09f5f0341a.lhr.life`. Auto-starts on boot.
- **WaTgBridge + THERAPY (2026-03-14 → 2026-03-15):** WhatsApp-to-Telegram bridge project - **CANCELLED**
  - Reason: Technical limitations with topic creation and complexity of configuration made it an insufficient solution
  - Deleted: 2026-03-15 11:24 UTC
- **x402charity Fix (2026-03-07):** Submitted a working Express example/fix to AllScale Lab (hi@allscale.io) to improve their documentation and integration flow.
- **Google Integration (2026-03-06):** Connected `bmnaorpop@gmail.com` using the `gog` skill. Keyring password is `1234`.

## Personal
- **Pet:** Popik (פופיק), the family dog. He's very cute, about 10 years old, and has a tendency to run away when released. (Corrected 2026-03-14).
- **Server:** VPS (srv1446922).
- **Home Assistant:** Connected to Alexa. Plan to automate morning radio (Galgalatz) at 07:00.

---
*Updated on 2026-03-06 by POP.*
