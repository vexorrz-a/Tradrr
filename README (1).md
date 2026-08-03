# 📈 Stock Market Simulator

A beautiful, interactive stock trading simulator with real-time market data. Buy and sell stocks, gold, silver, and more using real prices from Alpha Vantage.

## Features

✨ **Real-Time Data** - Live stock prices from Alpha Vantage API
💰 **Virtual Trading** - Start with $10,000 and practice trading
📊 **Portfolio Tracking** - Monitor your holdings in real-time
📋 **Transaction History** - Keep track of all your trades
🎨 **Beautiful UI** - Dark mode, responsive design
⚡ **Fast & Simple** - Built with Flask, no complex dependencies

## Screenshots

```
┌─────────────────────────────────────────────┐
│  📈 Stock Simulator  │  Portfolio: $12,500  │
├─────────────────────────────────────────────┤
│                                             │
│  🛒 Buy              │  💰 Sell            │
│  [Symbol] [Qty] [🔍] │  [Symbol] [Qty] [🔍]│
│  [     Buy    ]      │  [    Sell    ]     │
│                                             │
│  🎯 Your Holdings    │  📋 History         │
│  AAPL: 10 @ $150    │  BUY 10 AAPL       │
│  GOLD: 5 @ $2000    │  SELL 5 GOLD       │
│                                             │
└─────────────────────────────────────────────┘
```

## Quick Start

### 1. Clone & Setup
```bash
git clone <your-repo>
cd stock-simulator

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install flask requests python-dotenv
```

### 2. Get an API Key
- Go to [Alpha Vantage](https://www.alphavantage.co/)
- Sign up (free)
- Copy your API key

### 3. Configure
```bash
# Copy the example .env file
cp .env.example .env

# Edit .env and add your API key
# ALPHA_VANTAGE_API_KEY=your_key_here
```

### 4. Run
```bash
python app_clean.py
```

Then open: **http://localhost:5000** 🚀

## Usage

### Buy Stocks
1. Enter symbol (e.g., `AAPL`, `GOOGL`, `MSFT`)
2. Enter quantity
3. Click "Buy"

### Sell Stocks
1. Enter symbol you own
2. Enter quantity
3. Click "Sell"

### Check Prices
- Click "Check Price" to see real-time prices
- Works for stocks and commodities (`GOLD`, `SILVER`)

### View Portfolio
- Left side shows all your holdings
- Top bar shows total portfolio value and cash
- Updates every 5 seconds

## Supported Symbols

**Popular Stocks:**
- `AAPL` - Apple
- `GOOGL` - Google
- `MSFT` - Microsoft
- `TSLA` - Tesla
- `AMZN` - Amazon
- `META` - Meta
- `NVDA` - Nvidia
- ...and any stock supported by Alpha Vantage

**Commodities:**
- `GOLD` - Gold price
- `SILVER` - Silver price

## Project Structure

```
stock-simulator/
├── app_clean.py          # Flask backend (loads API key from .env)
├── templates/
│   └── index.html        # Web UI
├── .env.example          # Copy this and add your API key
├── .gitignore           # Don't commit sensitive files
├── README.md            # This file
└── SETUP.md             # Detailed setup guide
```

## Environment Variables

Create a `.env` file (copy from `.env.example`):
```
ALPHA_VANTAGE_API_KEY=your_free_api_key_here
```

**Never commit `.env` to git!** It's in `.gitignore` by default.

## API Limits

Alpha Vantage Free Tier:
- ✅ 5 API calls per minute
- ✅ 500 requests per day
- ✅ Unlimited after that (you just wait)

The simulator caches prices locally to avoid wasting calls.

## Troubleshooting

### "Could not fetch price"
- Check your `.env` file has the API key
- Make sure you're online
- Wait a few seconds (API rate limit)

### Port 5000 already in use
- Edit `app_clean.py` and change `port=5000` to `port=5001`

### `flask` not found
```bash
pip install flask requests python-dotenv --upgrade
```

### API key not working
- Get a new one from [Alpha Vantage](https://www.alphavantage.co/)
- Make sure it's in `.env` exactly: `ALPHA_VANTAGE_API_KEY=your_key`

## Technologies

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **API**: Alpha Vantage (Real stock data)
- **Styling**: Modern dark mode UI

## Tips for Trading

💡 Check prices before buying to see potential costs
💡 Use "Check Price" button to scout assets
💡 Transaction history helps you learn patterns
💡 Start small to understand the market
💡 Don't worry about losing—it's free! 😄

## Contributing

Feel free to fork, modify, and submit PRs!

Ideas:
- Add more commodities (crypto, forex)
- Save portfolio to database
- Add charts and analytics
- Multi-user support
- Mobile app

## License

MIT License - feel free to use however you want!

## Disclaimer

This is a **practice/educational simulator** only. No real money involved. Stock prices are real, but you're not actually buying/selling anything. Use this to learn before trading real money! 📚

---

Made with ❤️ for traders learning the market 📈
