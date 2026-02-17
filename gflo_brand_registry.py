import os
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()
w3 = Web3(Web3.HTTPProvider("https://ethereum-sepolia-rpc.publicnode.com"))
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
account = w3.eth.account.from_key(PRIVATE_KEY)

# A telepített ReformerModule címe (amit az előbb hoztunk létre)
REFORMER_MODULE = "0x..." # Ide illeszd be a ReformerModule címedet!

# ABI a márka regisztrációhoz
REFORMER_ABI = [
    {
        "inputs": [
            {"name": "brandName", "type": "string"},
            {"name": "metadataUri", "type": "string"}
        ],
        "name": "registerBrand",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

def register():
    print(f"🎨 GFLO Márka Bejegyzése: 'GFLO Creator'...")
    contract = w3.eth.contract(address=REFORMER_MODULE, abi=REFORMER_ABI)
    
    try:
        tx = contract.functions.registerBrand(
            "GFLO Creator Prime", 
            "ipfs://gflo-genesis-metadata"
        ).build_transaction({
            'from': account.address,
            'nonce': w3.eth.get_transaction_count(account.address),
            'gas': 300000,
            'gasPrice': w3.eth.gas_price
        })
        
        signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        print(f"⏳ Márka bejegyzése folyamatban... (Hash: {tx_hash.hex()})")
        w3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"💎 GRATULÁLUNK! A GFLO márkád hivatalosan is létezik a blokkláncon!")
        
    except Exception as e:
        print(f"❌ Hiba a regisztrációkor: {e}")

if __name__ == "__main__":
    register()
