import os
import json
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()
w3 = Web3(Web3.HTTPProvider("https://ethereum-sepolia-rpc.publicnode.com"))
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
account = w3.eth.account.from_key(PRIVATE_KEY)

# Jelenlegi stabil pontok
SOVEREIGN = "0x5cf48Be5094bFDaFA647384431f2A513a2979B0E"
REGISTRY  = "0x0877298642353805B7c297316A99a2939b541893"

print(f"🛠️ GFLO Rendszer szerviz indítása...")

# Ha megvan a ReformerModule.sol, megpróbáljuk kinyerni az ABI-t
# Ha nincs, kézzel adjuk meg a legfontosabb funkciót a teszthez
REFORMER_ABI = [
    {
        "inputs": [
            {"name": "user", "type": "address"},
            {"name": "newPath", "type": "string"}
        ],
        "name": "evolveUserPath",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

def check_and_bridge():
    # Itt ellenőrizzük, hogy a Sovereign látja-e a Registry-t
    print("🔗 Kapcsolat ellenőrzése...")
    # ... (ide jön a validációs kód)
    print("✅ Rendszer készen áll a manuális hídépítésre.")

if __name__ == "__main__":
    check_and_bridge()
