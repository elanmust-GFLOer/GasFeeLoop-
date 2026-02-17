import os
import json
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()
w3 = Web3(Web3.HTTPProvider("https://ethereum-sepolia-rpc.publicnode.com"))
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
account = w3.eth.account.from_key(PRIVATE_KEY)

# Címek a sikeres deploymented alapján
SOVEREIGN = "0x5cf48Be5094bFDaFA647384431f2A513a2979B0E"
REGISTRY  = "0x0877298642353805B7c297316A99a2939b541893"
PRAXIS    = "0x..." # Ide illeszd be a PraxisModule címedet, ha megvan!

# ABI-k a validációhoz
REG_ABI = [{"inputs":[{"name":"user","type":"address"}],"name":"getUserPath","outputs":[{"name":"","type":"string"}],"type":"function"}]
SOV_ABI = [{"inputs":[{"name":"user","type":"address"},{"name":"amount","type":"uint256"}],"name":"awardXP","outputs":[],"type":"function"}]

def run_baptism():
    print(f"🌿 GFLO Tűzkeresztség Indítása...")
    print(f"👤 Felhasználó: {account.address}")

    # 1. LÉPÉS: REGISTRY ELLENŐRZÉSE
    try:
        reg_contract = w3.eth.contract(address=REGISTRY, abi=REG_ABI)
        # Megnézzük, van-e már valamilyen státuszod
        path = reg_contract.functions.getUserPath(account.address).call()
        print(f"✅ Registry Validálva: Jelenlegi útvonalad: '{path}'")
    except Exception as e:
        print(f"⚠️ Registry info nem érhető el közvetlenül: {e}")

    # 2. LÉPÉS: XP/TOKEN OSZTÁS (A Sovereign-en keresztül)
    print(f"\n💎 Kísérlet az első GFLO elismerés kiosztására...")
    sov_contract = w3.eth.contract(address=SOVEREIGN, abi=SOV_ABI)
    
    try:
        # 100 egység XP/Token kiosztása (egyszerűsített hívás)
        tx = sov_contract.functions.awardXP(account.address, 100).build_transaction({
            'from': account.address,
            'nonce': w3.eth.get_transaction_count(account.address),
            'gas': 200000,
            'gasPrice': w3.eth.gas_price
        })
        
        signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        
        print(f"⏳ Tranzakció elküldve: {tx_hash.hex()}")
        print("Várjunk a blokklánc visszaigazolására...")
        w3.eth.wait_for_transaction_receipt(tx_hash)
        print("\n🏆 SIKER! A GFLO rendszer életre kelt: XP/Token kiosztva!")
        
    except Exception as e:
        print(f"❌ Aktiválási hiba: {e}")
        print("Tipp: Lehet, hogy a SovereignModule-ban 'setupUser' után 'award' a funkció neve?")

if __name__ == "__main__":
    run_baptism()
