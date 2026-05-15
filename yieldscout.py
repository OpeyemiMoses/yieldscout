import os
import requests
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# ---- Step 1: Fetch live yield data ----
def get_yield_data():
    print("Fetching live yield data from DeFiLlama...")
    url = "https://yields.llama.fi/pools"
    response = requests.get(url)
    data = response.json()
    pools = data["data"]

    filtered = [
        p for p in pools
        if p.get("tvlUsd", 0) > 1_000_000
        and p.get("apy", 0) > 5
        and p.get("apy", 0) < 300
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


# ---- Step 2: Persona prompts ----
PERSONAS = {
    "retail": """You are YieldScout in RETAIL MODE.

Your audience is everyday DeFi users — beginners to intermediate. They want simple, safe, actionable advice.

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

Your audience is crypto-native DeFi veterans. They understand impermanent loss, CLMM positions, TVL dynamics, and protocol risk.

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

Your audience is DAOs and treasury managers deploying large capital ($500K+). They prioritize capital preservation, protocol reputation, and sustainable yield over chasing APY.

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


# ---- Step 3: Run YieldScout with persona ----
def run_yieldscout(pools, mode="retail"):
    client = OpenAI(
        api_key=os.getenv("SWARMS_API_KEY"),
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
                "content": f"Here is the current live yield data from DeFiLlama. Produce your report:\n\n{data_str}"
            }
        ],
        max_tokens=1024,
    )

    return response.choices[0].message.content


# ---- Step 4: Main ----
if __name__ == "__main__":
    pools = get_yield_data()

    print("\n🔍 Select your mode:")
    print("  1 - Retail (beginner-friendly)")
    print("  2 - Power User (advanced DeFi)")
    print("  3 - DAO / Treasury (institutional)\n")

    choice = input("Enter 1, 2, or 3: ").strip()

    mode_map = {"1": "retail", "2": "power", "3": "dao"}
    mode = mode_map.get(choice, "retail")

    print(f"\nYieldScout ({mode.upper()} MODE) is analyzing the market...\n")
    report = run_yieldscout(pools, mode=mode)

    print(f"\n========== YIELDSCOUT REPORT [{mode.upper()}] ==========\n")
    print(report)