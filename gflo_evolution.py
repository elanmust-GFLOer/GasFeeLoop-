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
REFORMER  = "0x..." # Ide másold a ReformerModule címedet!
REGISTRY  = "0x0877298642353805B7c297316A99a2939b541893"

# Reformer híd ABI
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

reformer_contract = w3.eth.contract(address=REFORMER, abi=REFORMER_ABI)

def evolve():
    print(f"🧬 GFLO Evolúció: Szintlépés indítása...")
    new_status = "GFLO_CONTRIBUTOR_LEVEL_1"
    
    try:
        # A ReformerModule-on keresztül kérjük a szintlépést
        tx = reformer_contract.functions.evolveUserPath(account.address, new_status).build_transaction({
            'from': account.address,
            'nonce': w3.eth.get_transaction_count(account.address),
            'gas': 250000,
            'gasPrice': w3.eth.gas_price
        })

        signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        
        print(f"⏳ Az evolúció folyamatban... (Hash: {tx_hash.hex()})")
        w3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"✨ GRATULÁLUNK! A profilod szintet lépett: {new_status}")
        
    except Exception as e:
        print(f"❌ Az evolúció megakadt: {e}")
        print("Tipp: Ellenőrizd, hogy a ReformerModule-nak is adtunk-e már jogot a Registry-ben!")

if __name__ == "__main__":
    evolve()
