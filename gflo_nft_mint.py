import os
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()
w3 = Web3(Web3.HTTPProvider("https://ethereum-sepolia-rpc.publicnode.com"))
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
account = w3.eth.account.from_key(PRIVATE_KEY)

# Validált ReformerModule címe (a legutóbbi sikeres futtatásodból)
REFORMER_MODULE = "0x..." # Ide másold be a reformer_address.txt tartalmát!

# ReformerModule ABI (a minteléshez és kollekciókészítéshez szükséges funkciók)
REFORMER_ABI = [
    {"inputs":[{"name":"collectionName","type":"string"},{"name":"collectionSymbol","type":"string"},{"name":"collectionUri","type":"string"}],"name":"createNFTCollection","outputs":[{"name":"","type":"address"}],"stateMutability":"nonpayable","type":"function"},
    {"inputs":[{"name":"tokenUri","type":"string"}],"name":"mintBrandNFT","outputs":[{"name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"}
]

def mint_genesis():
    contract = w3.eth.contract(address=REFORMER_MODULE, abi=REFORMER_ABI)
    
    print(f"📦 1. Lépés: 'Elan Must GFLOer' NFT Kollekció létrehozása...")
    # Kollekció létrehozása (csak egyszer kell)
    tx_coll = contract.functions.createNFTCollection(
        "Elan Must GFLOer Collection", 
        "EMG", 
        "ipfs://gflo-elan-collection"
    ).build_transaction({
        'from': account.address,
        'nonce': w3.eth.get_transaction_count(account.address),
        'gas': 2000000,
        'gasPrice': w3.eth.gas_price
    })
    
    signed_coll = w3.eth.account.sign_transaction(tx_coll, PRIVATE_KEY)
    hash_coll = w3.eth.send_raw_transaction(signed_coll.raw_transaction)
    print(f"⏳ Kollekció telepítése folyamatban... (Hash: {hash_coll.hex()})")
    w3.eth.wait_for_transaction_receipt(hash_coll)
    
    print(f"🎨 2. Lépés: Az első történelmi NFT veretése (Minting)...")
    # Első NFT veretése a metaadatokkal
    tx_mint = contract.functions.mintBrandNFT(
        "ipfs://Qme...ElanMustGFLOer_Genesis_1"
    ).build_transaction({
        'from': account.address,
        'nonce': w3.eth.get_transaction_count(account.address),
        'gas': 500000,
        'gasPrice': w3.eth.gas_price
    })
    
    signed_mint = w3.eth.account.sign_transaction(tx_mint, PRIVATE_KEY)
    hash_mint = w3.eth.send_raw_transaction(signed_mint.raw_transaction)
    print(f"⏳ NFT veretése folyamatban... (Hash: {hash_mint.hex()})")
    w3.eth.wait_for_transaction_receipt(hash_mint)
    
    print(f"💎 GRATULÁLUNK! Az első 'Elan Must GFLOer' NFT rögzítve a blokkláncon!")

if __name__ == "__main__":
    mint_genesis()
