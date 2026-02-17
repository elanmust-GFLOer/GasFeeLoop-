import json
import os
import re
from web3 import Web3
from eth_abi import encode
from dotenv import load_dotenv

load_dotenv()

w3 = Web3(Web3.HTTPProvider("https://ethereum-sepolia-rpc.publicnode.com"))
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
account = w3.eth.account.from_key(PRIVATE_KEY)

def super_clean_hex(name, raw_str):
    # CSAK a 0-9 és a-f karaktereket tartjuk meg. Minden mást (szóköz, \n, \r) kidobunk.
    clean = re.sub(r'[^a-fA-F0-9]', '', raw_str)
    # Ha véletlenül 0x-szel kezdődne, azt is levágjuk az elejéről a bájttá alakításhoz
    if clean.lower().startswith('0x'):
        clean = clean[2:]
    
    # Ellenőrizzük a hosszt (40 karakter = 20 bájt)
    if len(clean) != 40:
        print(f"⚠️ Figyelem: {name} hossza nem 40 karakter, hanem {len(clean)}! Javítás...")
        clean = clean[:40] # Kényszerített vágás, ha túlfutna láthatatlan karakter miatt
        
    addr_bytes = bytes.fromhex(clean)
    print(f"🧬 {name} tisztítva és bájttá alakítva.")
    return addr_bytes

def deploy():
    try:
        # A címek kényszerített tisztítása
        reg_bytes = super_clean_hex("Registry", "0x877298642353805b7c297316a99a2939b5418935")
        tok_bytes = super_clean_hex("Token",    "0x563b2e3b499818a2f84c472efb3169a2667807fe")
        tre_bytes = super_clean_hex("Treasury", "0x80a456710b7af746d88733dc456bc3190e6fa31")

        with open("compiled_sovereign.json", "r") as f:
            data = json.load(f)
        
        # Biztonsági ellenőrzés a JSON struktúrára
        contract_path = "SovereignModule.sol:SovereignModule"
        contract_info = data["contracts"][contract_path]
        bytecode = contract_info["bin"]

        print(f"🛠️ ABI kódolás...")
        encoded_args = encode(['address', 'address', 'address'], [reg_bytes, tok_bytes, tre_bytes])
        full_data = "0x" + bytecode + encoded_args.hex()

        tx = {
            'from': account.address,
            'nonce': w3.eth.get_transaction_count(account.address),
            'gasPrice': int(w3.eth.gas_price * 1.5),
            'data': full_data,
            'value': 0,
            'chainId': 11155111
        }
        
        tx['gas'] = int(w3.eth.estimate_gas(tx) * 1.2)
        signed = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
        
        print(f"⏳ Küldés... Hash: {tx_hash.hex()}")
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=300)
        print(f"\n✅ SIKER! Szerződés címe: {receipt.contractAddress}")

    except Exception as e:
        print(f"\n❌ Hiba: {str(e)}")

if __name__ == "__main__":
    deploy()
