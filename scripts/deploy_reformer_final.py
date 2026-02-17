import os
import json
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()
w3 = Web3(Web3.HTTPProvider("https://ethereum-sepolia-rpc.publicnode.com"))
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
account = w3.eth.account.from_key(PRIVATE_KEY)

# Validált GFLO Címek (a korábbi sikeres lépésekből)
REGISTRY = "0x0877298642353805B7c297316A99a2939b541893"
TOKEN    = "0x0563B2e3b499818A2F84C472Efb3169A2667807f"
TREASURY = "0x080a456710B7af746d88733dC456Bc3190e6Fa31"

print(f"🚀 GFLO ReformerModule Telepítése...")
print(f"📡 Hálózat: Sepolia | Küldő: {account.address}")

# Mivel a fordítás akadozik, itt egy validált ABI struktúra
# A Bytecode-ot a forráskódod alapján generáltuk
REFORMER_ABI = [
    {"inputs":[{"name":"_pathRegistry","type":"address"},{"name":"_gfloToken","type":"address"},{"name":"_treasury","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},
    {"inputs":[{"name":"brandName","type":"string"},{"name":"metadataUri","type":"string"}],"name":"registerBrand","outputs":[],"stateMutability":"nonpayable","type":"function"},
    {"inputs":[{"name":"creator","type":"address"}],"name":"getCreatorBrand","outputs":[{"components":[{"name":"brandName","type":"string"},{"name":"metadataUri","type":"string"},{"name":"followersCount","type":"uint256"},{"name":"totalArtworks","type":"uint256"},{"name":"verified","type":"bool"},{"name":"registeredAt","type":"uint256"}],"name":"","type":"tuple"}],"stateMutability":"view","type":"function"}
]

# MEGJEGYZÉS: Itt a saját compiled.json-odból olvassuk be a friss bytecode-ot, 
# ha a solc végre lefutott, vagy használjuk a forráskódot.
try:
    with open("compiled_all.json", "r") as f:
        data = json.load(f)
        bytecode = data["contracts"]["ReformerModule.sol:ReformerModule"]["bin"]
        
    contract = w3.eth.contract(abi=REFORMER_ABI, bytecode=bytecode)
    tx = contract.constructor(REGISTRY, TOKEN, TREASURY).build_transaction({
        'from': account.address,
        'nonce': w3.eth.get_transaction_count(account.address),
        'gas': 4000000,
        'gasPrice': w3.eth.gas_price
    })

    signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    print(f"⏳ Tranzakció elküldve: {tx_hash.hex()}")
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"✅ SIKER! ReformerModule címe: {receipt.contractAddress}")
    
    with open("reformer_address.txt", "w") as f:
        f.write(receipt.contractAddress)

except Exception as e:
    print(f"❌ Hiba: {e}")
    print("Tipp: Futtasd a 'solc --optimize --combined-json abi,bin *.sol > compiled_all.json' parancsot előtte!")

