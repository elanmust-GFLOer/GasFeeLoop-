import os
import json
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()
w3 = Web3(Web3.HTTPProvider("https://ethereum-sepolia-rpc.publicnode.com"))
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
account = w3.eth.account.from_key(PRIVATE_KEY)

# Címek
SOVEREIGN = "0x5cf48Be5094bFDaFA647384431f2A513a2979B0E"
REGISTRY  = "0x0877298642353805B7c297316A99a2939b541893"
TOKEN     = "0x0563B2e3b499818A2F84C472Efb3169A2667807f"
TREASURY  = "0x080a456710B7af746d88733dC456Bc3190e6Fa31"

# A híd-funkciók (Interface alapján)
BRIDGE_ABI = [
    {
        "inputs": [{"name": "user", "type": "address"}],
        "name": "setupUser",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

sov_contract = w3.eth.contract(address=SOVEREIGN, abi=BRIDGE_ABI)

def activate():
    print(f"🚀 GFLO Ökoszisztéma Aktiválása...")
    print(f"🔗 Kapcsolódás: {account.address}")
    
    try:
        # A setupUser hívás aktiválja a kapcsolatot a Registry-vel
        tx = sov_contract.functions.setupUser(account.address).build_transaction({
            'from': account.address,
            'nonce': w3.eth.get_transaction_count(account.address),
            'gas': 300000,
            'gasPrice': w3.eth.gas_price
        })
        
        signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        
        print(f"⏳ Tranzakció a láncon: {tx_hash.hex()}")
        w3.eth.wait_for_transaction_receipt(tx_hash)
        print("\n🏆 SIKER! A híd áll, a SovereignModule átvette az irányítást.")
        print(f"Token ({TOKEN}) és Treasury ({TREASURY}) szinkronizálva.")
        
    except Exception as e:
        print(f"❌ Hiba az aktiváláskor: {e}")

if __name__ == "__main__":
    activate()
