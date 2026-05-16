# YieldScout 🔍

> Live DeFi yield intelligence — personalized by your wallet.

YieldScout is an AI-powered DeFi research agent that reads your on-chain stablecoin balance across 6 major EVM chains, automatically assigns your investor profile, and delivers a sharp, actionable yield report — all in one run.

No manual selection. No guesswork. Just connect your wallet and get your report.

---

## What It Does

Every run, YieldScout:
1. Scans your wallet across Ethereum, Arbitrum, Base, Optimism, Polygon, and Avalanche
2. Detects your total stablecoin balance (USDC, USDT, DAI, FRAX, and more)
3. Automatically assigns your investor persona based on balance
4. Fetches live yield data across 500+ DeFi protocols via DeFiLlama
5. Delivers a structured research report tailored to your profile

---

## Auto Persona Assignment

YieldScout reads your wallet and assigns your mode automatically:

| Balance | Persona | Style |
|---------|---------|-------|
| Under $5,000 | 🟢 Retail | Simple, safe, plain English |
| $5,000 - $100,000 | 🔴 Power User | Technical, deep, alpha-focused |
| Above $100,000 | 🔵 DAO / Treasury | Formal, conservative, capital-aware |

---

## How To Run Locally

**1. Clone the repo**
git clone https://github.com/OpeyemiMoses/yieldscout.git
cd yieldscout

**2. Create virtual environment**
python -m venv venv
venv\Scripts\activate

**3. Install dependencies**
pip install -r requirements.txt

**4. Add your API key**

Create a `.env` file:
SWARMS_API_KEY=your_swarms_api_key_here
DEBANK_API_KEY=your_debank_api_key_here

**5. Run the agent**
python yieldscout.py

**6. Enter your wallet address when prompted**
Enter your wallet address: 0xYourWalletHere

---

YieldScout handles everything else automatically.

---

## Tech Stack

- **Python** — core language
- **DeBank Cloud API** — multi-chain stablecoin balance scanning
- **DeFiLlama API** — live yield data (free, no key needed)
- **Swarms API** — AI agent brain
- **OpenAI-compatible endpoint** — via Swarms

## Supported Chains

- Ethereum
- Arbitrum
- Base
- Optimism
- Polygon
- Avalanche

## Supported Stablecoins

USDC, USDT, DAI, BUSD, FRAX, LUSD, USDD, TUSD, USDP, GUSD

---

## Live On Swarms Marketplace

> [YieldScout on Swarms Marketplace](#) — link coming soon

---

Built for the ACM Hackathon on Swarms Marketplace — May 2026.