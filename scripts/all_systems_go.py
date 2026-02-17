import json
import os
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()
w3 = Web3(Web3.HTTPProvider("https://ethereum-sepolia-rpc.publicnode.com"))

# Címek (A te sikeres deploymentjeid alapján)
SOVEREIGN = "0x5cf48Be5094bFDaFA647384431f2A513a2979B0E"
REGISTRY  = "0x0877298642353805B7c297316A99a2939b541893"
TOKEN     = "0x0563B2e3b499818A2F84C472Efb3169A2667807f"
TREASURY  = "0x080a456710B7af746d88733dC456Bc3190e6Fa31"

ADMIN_ROLE = "0x0000000000000000000000000000000000000000000000000000000000000000"

# Minimális ABI-k a teszteléshez
ABI_REG = [{"inputs":[{"name":"role","type":"bytes32"},{"name":"account","type":"address"}],"name":"hasRole","outputs":[{"name":"","type":"bool"}],"type":"function"}]
ABI_TOK = [{"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"type":"function"}, {"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"type":"function"}]
ABI_TRE = [{"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"type":"function"}]

def run_report():
    print("🛰️  GFLO ÖKOSZISZTÉMA JELENTÉS - ALL SYSTEMS GO\n" + "="*45)
    
    # 1. REGISTRY VALIDÁCIÓ (A hatalom központja)
    reg_contract = w3.eth.contract(address=REGISTRY, abi=ABI_REG)
    is_admin = reg_contract.functions.hasRole(ADMIN_ROLE, SOVEREIGN).call()
    print(f"🏛️  Registry Jogosultság:  {'✅ AKTÍV (Sovereign is Admin)' if is_admin else '❌ HIÁNYZIK'}")

    # 2. TOKEN VALIDÁCIÓ (Az üzemanyag)
    try:
        tok_contract = w3.eth.contract(address=TOKEN, abi=ABI_TOK)
        name = tok_contract.functions.name().call()
        symbol = tok_contract.functions.symbol().call()
        print(f"🪙  Token Állapot:        ✅ ÉL ({name} [{symbol}])")
    except:
        print("🪙  Token Állapot:        ⚠️ Kapcsolódási hiba")

    # 3. TREASURY VALIDÁCIÓ (A kincstár)
    try:
        tre_contract = w3.eth.contract(address=TREASURY, abi=ABI_TRE)
        # Itt nézzük meg, ki a tulajdonosa a kincstárnak
        # Ideális esetben a Sovereign-nek kellene lennie később
        tre_owner = tre_contract.functions.owner().call()
        print(f"💰  Treasury Gazda:      👤 {tre_owner[:10]}...")
    except:
        print("💰  Treasury Állapot:     ⚠️ Nem lekérdezhető")

    print("="*45)
    if is_admin:
        print("\n🚀 KONKLÚZIÓ: A GFLO RENDSZER ÜZEMKÉSZ!")
    else:
        print("\n⚠️ KONKLÚZIÓ: TOVÁBBI HÍZALOZÁS SZÜKSÉGES.")

if __name__ == "__main__":
    run_report()
