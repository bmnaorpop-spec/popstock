const express = require('express');
const { x402charity } = require('x402charity');
const app = express();

// x402charity middleware setup
// This middleware will automatically handle micro-donations to charities
app.use(x402charity({
  charityId: 'testing-charity', // As requested in the bounty
  donationAmount: 0.01,         // Amount in USDC per action
  network: 'base'               // Base network as per documentation
}));

app.get('/', (req, res) => {
  res.send('<h1>x402charity Express Example</h1><p>Every visit to this page triggers a micro-donation!</p>');
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Example app listening on port ${PORT}`);
});
