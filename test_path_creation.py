import os
import json
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()
w3 = Web3(Web3.HTTPProvider("https://ethereum-sepolia-rpc.publicnode.com"))
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
account = w3.eth.account.from_key(PRIVATE_KEY)

# A SovereignModule címe (ő az admin a Registry-ben)
SOVEREIGN = "0x5cf48Be5094bFDaFA647384431f2A513a2979B0E"

# Betöltjük a Sovereign ABI-t
with open("compiled_sovereign.json", "r") as f:
    data = json.load(f)
    abi = data["contracts"]["SovereignModule.sol:SovereignModule"]["abi"]

contract = w3.eth.contract(address=SOVEREIGN, abi=abi)

print(f"🚀 GFLO Funkcionális Teszt: Új útvonal regisztrálása...")

try:
    # Meghívjuk a SovereignModule-on keresztül a Registry-t
    # Feltételezve, hogy van egy registerPath vagy hasonló függvényed
    # Ha más a neve (pl. createProfile), írd át!
    tx = contract.functions.registerUserPath(account.address).build_transaction({
        'from': account.address,
        'nonce': w3.eth.get_transaction_count(account.address),
        'gas': 200000,
        'gasPrice': w3.eth.gas_price
    })

    signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    
    print(f"⏳ Tranzakció elküldve: {tx_hash.hex()}")
    w3.eth.wait_for_transaction_receipt(tx_hash)
    print("✅ SIKER! A SovereignModule végrehajtotta az első parancsát a Registry-ben.")
except Exception as e:
    print(f"❌ Teszt hiba: {e}")
    print("Tipp: Ellenőrizd a SovereignModule.sol-ban a pontos függvénynévre (pl. setupUser)!")
