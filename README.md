# YieldScout 🔍

> Live DeFi yield intelligence for every type of investor.

YieldScout is an AI-powered DeFi research agent that pulls real-time yield data from DeFiLlama, filters out noise, and delivers sharp, actionable reports — tailored to your investor profile.

---

## What It Does

Every run, YieldScout:
- Fetches live yield data across 500+ DeFi protocols
- Filters by TVL (min $1M) and APY (max 300%) to remove suspicious pools
- Ranks the top 20 opportunities
- Runs AI analysis via the Swarms API
- Delivers a structured research report in your chosen mode

---

## Three Persona Modes

| Mode | For Who | Style |
|------|---------|-------|
| 🟢 Retail | Everyday DeFi users | Simple, safe, plain English |
| 🔴 Power User | DeFi veterans | Technical, deep, alpha-focused |
| 🔵 DAO / Treasury | Institutions & DAOs | Formal, conservative, capital-aware |

---

## How To Run Locally

**1. Clone the repo**
git clone https://github.com/OpeyemiMoses/yieldscout.git cd yieldscout

**2. Create virtual environment**
python -m venv venv
venv\Scripts\activate

**3. Install dependencies**
pip install -r requirements.txt

**4. Add your API key**

Create a `.env` file:
SWARMS_API_KEY=your_swarms_api_key_here

**5. Run the agent**
python yieldscout.py

---

## Tech Stack

- **Python** — core language
- **DeFiLlama API** — live yield data (free, no key needed)
- **Swarms API** — AI agent brain
- **OpenAI-compatible endpoint** — via Swarms

---

## Live On Swarms Marketplace

> [YieldScout on Swarms Marketplace](#) — link coming soon

---

Built for the ACM Hackathon on Swarms Marketplace — May 2026.