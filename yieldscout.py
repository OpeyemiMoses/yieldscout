import os
import requests
import json
import httpx
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

DEBANK_API_KEY = os.getenv("DEBANK_API_KEY")
SWARMS_API_KEY = os.getenv("SWARMS_API_KEY")

# Supported stablecoins
STABLES = {"usdc", "usdt", "dai", "busd", "frax", "lusd", "usdd", "tusd", "usdp", "gusd"}

# ---- Step 1: Get wallet stablecoin balance across chains ----
def get_stable_balance(wallet_address):
    print(f"\nScanning wallet: {wallet_address}")
    print("Checking stablecoin balances across Ethereum, Arbitrum, Base, Optimism, Polygon, Avalanche...\n")

    url = "https://pro-openapi.debank.com/v1/user/all_token_list"
    headers = {
        "accept": "application/json",
        "AccessKey": DEBANK_API_KEY
    }
    params = {
        "id": wallet_address,
        "is_all": "false"
    }

    response = httpx.get(url, headers=headers, params=params)
    tokens = response.json()

    total_stable_usd = 0
    stable_breakdown = []

    for token in tokens:
        if not isinstance(token, dict):
            continue
        symbol = token.get("symbol", "").lower()
        amount = token.get("amount", 0)
        price = token.get("price", 0)
        chain = token.get("chain", "unknown")
        usd_value = amount * price

        if any(stable in symbol for stable in STABLES) and usd_value > 1:
            total_stable_usd += usd_value
            stable_breakdown.append({
                "token": token.get("symbol"),
                "chain": chain,
                "amount": round(amount, 2),
                "usd_value": round(usd_value, 2)
            })

    return total_stable_usd, stable_breakdown


# ---- Step 2: Assign persona based on balance ----
def assign_persona(total_stable_usd):
    if total_stable_usd < 5000:
        return "retail"
    elif total_stable_usd < 100000:
        return "power"
    else:
        return "dao"


# ---- Step 3: Fetch live yield data ----
def get_yield_data():
    print("Fetching live yield data from DeFiLlama...")
    url = "https://yields.llama.fi/pools"
    response = requests.get(url)
    data = response.json()
    pools = data["data"]

    # EVM chains only — Solana excluded (wallet scanner is EVM-only)
    EVM_CHAINS = {"Ethereum", "Arbitrum", "Base", "Optimism", "Polygon", "Avalanche"}

    filtered = [
        p for p in pools
        if p.get("tvlUsd", 0) > 1_000_000
        and p.get("apy", 0) > 5
        and p.get("apy", 0) < 300
        and p.get("chain") in EVM_CHAINS
    ]

    sorted_pools = sorted(filtered, key=lambda x: x["apy"], reverse=True)
    top_pools = sorted_pools[:20]

    results = []
    for p in top_pools:
        results.append({
            "protocol": p.get("project", "Unknown"),
            "chain": p.get("chain", "Unknown"),
            "pool": p.get("symbol", "Unknown"),
            "apy": round(p.get("apy", 0), 2),
            "tvl_usd": round(p.get("tvlUsd", 0), 2),
        })

    return results


# ---- Step 4: Persona prompts ----
PERSONAS = {
    "retail": """You are YieldScout in RETAIL MODE.

Your audience is everyday DeFi users with smaller balances under $5,000. They want simple, safe, actionable advice.

Analyze the yield data and respond with:

1. TOP 3 PICKS FOR YOU
   - Focus on stablecoins or well-known assets (ETH, BTC, USDC, SOL)
   - Avoid small unknown chains
   - Explain each pick in 1-2 plain English sentences
   - Show APY and where to go

2. ONE TO WATCH
   - One slightly higher risk pick with upside potential
   - Explain the risk simply

3. SAFETY REMINDER
   - One line about DeFi risk in general

Keep it friendly, simple, and encouraging. No jargon.""",

    "power": """You are YieldScout in POWER USER MODE.

Your audience is crypto-native DeFi veterans with $5,000 - $100,000 in stablecoins. They understand impermanent loss, CLMM positions, TVL dynamics, and protocol risk.

Analyze the yield data and respond with:

1. TOP 5 HIGH-YIELD PLAYS
   - Full breakdown: protocol, chain, pool, APY, TVL
   - Risk commentary: IL exposure, protocol age, TVL stability
   - Entry notes: concentrated liquidity range considerations if applicable

2. CHAIN SPOTLIGHT
   - Which chain is dominating yields right now and why

3. RED FLAGS
   - Any pools that look suspicious (APY too high vs TVL, unknown protocols)

4. ALPHA SUMMARY
   - One sharp sentence on where the smart money is moving

Be direct, technical, and sharp. Assume full DeFi literacy.""",

    "dao": """You are YieldScout in DAO / TREASURY MODE.

Your audience is DAOs and treasury managers with over $100,000 in stablecoins. They prioritize capital preservation, protocol reputation, and sustainable yield.

Analyze the yield data and respond with:

1. TOP 3 TREASURY ALLOCATIONS
   - Only suggest protocols with TVL above $3M
   - Prioritize Uniswap, Aave, Curve, Balancer, Yearn, or equivalent blue chips
   - Include: protocol, chain, pool, APY, TVL, and a 2-sentence rationale
   - Note any governance or smart contract risk

2. DIVERSIFICATION STRATEGY
   - Suggest how to split capital across 2-3 of the picks
   - Consider chain diversification

3. RISK ASSESSMENT
   - Overall market yield environment in 2-3 sentences
   - Any macro concerns worth flagging

Be formal, precise, and risk-conscious. This is institutional-grade advice."""
}


# ---- Step 5: Run YieldScout ----
def run_yieldscout(pools, mode, wallet_summary):
    client = OpenAI(
        api_key=SWARMS_API_KEY,
        base_url="https://api.swarms.world/v1"
    )

    data_str = json.dumps(pools, indent=2)
    system_prompt = PERSONAS.get(mode, PERSONAS["retail"])

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": f"""Wallet Summary:
{wallet_summary}

Live yield data from DeFiLlama:
{data_str}

Produce your full research report based on this wallet's profile and the current yield opportunities."""
            }
        ],
        max_tokens=1024,
    )

    return response.choices[0].message.content


# ---- Step 6: Main ----
if __name__ == "__main__":
    wallet = input("Enter your wallet address: ").strip()

    total_stable, breakdown = get_stable_balance(wallet)

    if total_stable == 0:
        print("No stablecoin balance detected across major chains.")
        print("Defaulting to Retail Mode.\n")
        mode = "retail"
        wallet_summary = "Wallet has no detected stablecoin balance."
    else:
        mode = assign_persona(total_stable)
        wallet_summary = f"Total stablecoin balance: ${total_stable:,.2f}\n\nBreakdown:\n"
        for item in breakdown:
            wallet_summary += f"  - {item['token']} on {item['chain']}: ${item['usd_value']:,.2f}\n"

    print(f"Total Stablecoin Balance: ${total_stable:,.2f}")
    print(f"Assigned Persona: {mode.upper()} MODE\n")

    pools = get_yield_data()

    print(f"YieldScout ({mode.upper()} MODE) is analyzing the market...\n")
    report = run_yieldscout(pools, mode, wallet_summary)

    print(f"\n========== YIELDSCOUT REPORT [{mode.upper()}] ==========\n")
    print(report)