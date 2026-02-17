import os
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()
w3 = Web3(Web3.HTTPProvider("https://ethereum-sepolia-rpc.publicnode.com"))
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
account = w3.eth.account.from_key(PRIVATE_KEY)

# A korábbi sikeres deploy alapján a ReformerModule címe
# Megjegyzés: A 1000023268.jpg alapján a telepítés sikeres volt
REFORMER_MODULE = "0x0123456789ABCDEF0123456789ABCDEF01234567" # FRISSÍTSD A TERMINÁLODBAN LÁTOTT CÍMMEL!

REFORMER_ABI = [
    {"inputs":[{"name":"collectionName","type":"string"},{"name":"collectionSymbol","type":"string"},{"name":"collectionUri","type":"string"}],"name":"createNFTCollection","outputs":[{"name":"","type":"address"}],"stateMutability":"nonpayable","type":"function"},
    {"inputs":[{"name":"tokenUri","type":"string"}],"name":"mintBrandNFT","outputs":[{"name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"}
]

def run_mint():
    # Ha a reformer_address.txt létezik, beolvassuk belőle
    addr = REFORMER_MODULE
    if os.path.exists("reformer_address.txt"):
        with open("reformer_address.txt", "r") as f:
            addr = f.read().strip()

    print(f"📡 Csatlakozás a ReformerModule-hoz: {addr}")
    contract = w3.eth.contract(address=addr, abi=REFORMER_ABI)
    
    try:
        print(f"📦 Kollekció létrehozása: 'Elan Must GFLOer'...")
        nonce = w3.eth.get_transaction_count(account.address)
        
        tx = contract.functions.createNFTCollection(
            "Elan Must GFLOer Collection", "EMG", "ipfs://gflo-elan"
        ).build_transaction({
            'from': account.address,
            'nonce': nonce,
            'gas': 1500000,
            'gasPrice': w3.eth.gas_price
        })
        
        signed = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
        print(f"⏳ Tranzakció: {tx_hash.hex()}")
        w3.eth.wait_for_transaction_receipt(tx_hash)
        
        print(f"💎 NFT Veretése: Genezis #1...")
        mint_tx = contract.functions.mintBrandNFT(
            "ipfs://elan-must-gfloer-genesis-1"
        ).build_transaction({
            'from': account.address,
            'nonce': nonce + 1,
            'gas': 500000,
            'gasPrice': w3.eth.gas_price
        })
        
        signed_mint = w3.eth.account.sign_transaction(mint_tx, PRIVATE_KEY)
        w3.eth.send_raw_transaction(signed_mint.raw_transaction)
        print(f"🏆 SIKER! Az első NFT úton van a láncra!")

    except Exception as e:
        print(f"❌ Hiba: {e}")

if __name__ == "__main__":
    run_mint()
