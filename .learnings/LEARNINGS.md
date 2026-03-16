# 2026-03-13 - Learning: Avoiding Double Messages

- **Issue:** Barak pointed out that I sometimes send messages twice.
- **Root Cause:** I used the `message` tool to send a proactive update and then followed up with a similar message in the `<final>` block. On Telegram, this results in two messages.
- **Correction:** If using the `message` tool to deliver the final response to the user in the current session, the actual tool call response should be `NO_REPLY` to prevent the platform from sending a second copy of the final block. Or better, just use the `<final>` block for the direct reply and save `message` for other channels/sessions.
