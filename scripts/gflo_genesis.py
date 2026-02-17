import os
import json
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()
w3 = Web3(Web3.HTTPProvider("https://ethereum-sepolia-rpc.publicnode.com"))
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
account = w3.eth.account.from_key(PRIVATE_KEY)

# Validált GFLO Alapcímek
REGISTRY = "0x0877298642353805B7c297316A99a2939b541893"
TOKEN    = "0x0563B2e3b499818A2F84C472Efb3169A2667807f"
TREASURY = "0x080a456710B7af746d88733dC456Bc3190e6Fa31"

# Megpróbáljuk kinyerni a bytecode-ot a compiled_all.json-ból
try:
    with open("compiled_all.json", "r") as f:
        data = json.load(f)
        reformer_key = [k for k in data["contracts"].keys() if "ReformerModule.sol:ReformerModule" in k][0]
        abi = data["contracts"][reformer_key]["abi"]
        bytecode = data["contracts"][reformer_key]["bin"]
except Exception as e:
    print(f"❌ Hiba a bytecode beolvasásakor: {e}")
    exit()

def genesis():
    print(f"🌟 GFLO Genezis Indítása...")
    
    # 1. TELEPÍTÉS
    Reformer = w3.eth.contract(abi=abi, bytecode=bytecode)
    tx = Reformer.constructor(REGISTRY, TOKEN, TREASURY).build_transaction({
        'from': account.address,
        'nonce': w3.eth.get_transaction_count(account.address),
        'gas': 4000000,
        'gasPrice': w3.eth.gas_price
    })
    
    signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    print(f"⏳ ReformerModule telepítése... (Hash: {tx_hash.hex()})")
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    reformer_address = receipt.contractAddress
    print(f"✅ ReformerModule aktív: {reformer_address}")

    # 2. MÁRKA BEJEGYZÉSE
    print(f"🎨 Márka alapítása: 'Elan Must GFLOer'...")
    contract = w3.eth.contract(address=reformer_address, abi=abi)
    
    brand_tx = contract.functions.registerBrand(
        "Elan Must GFLOer", 
        "ipfs://gflo-genesis-elon-style"
    ).build_transaction({
        'from': account.address,
        'nonce': w3.eth.get_transaction_count(account.address),
        'gas': 500000,
        'gasPrice': w3.eth.gas_price
    })
    
    signed_brand = w3.eth.account.sign_transaction(brand_tx, PRIVATE_KEY)
    brand_hash = w3.eth.send_raw_transaction(signed_brand.raw_transaction)
    w3.eth.wait_for_transaction_receipt(brand_hash)
    
    print(f"🏆 SIKER! Az 'Elan Must GFLOer' márka rögzítve a blokkláncon!")
    print(f"📍 ReformerModule címe elmentve: reformer_address.txt")
    with open("reformer_address.txt", "w") as f:
        f.write(reformer_address)

if __name__ == "__main__":
    genesis()
