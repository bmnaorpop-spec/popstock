# x402charity Express Basic Example

This is a minimal example demonstrating how to integrate `x402charity` middleware into a basic Express.js application.

## Setup

1. Install dependencies:
   ```bash
   npm install
   ```

2. Start the server:
   ```bash
   node index.js
   ```

3. Visit `http://localhost:3000` to see it in action.

## How it works

The middleware is configured in `index.js`:

```javascript
app.use(x402charity({
  charityId: 'testing-charity',
  donationAmount: 0.01,
  network: 'base'
}));
```

Every request to the server will now trigger a micro-donation flow managed by x402.
