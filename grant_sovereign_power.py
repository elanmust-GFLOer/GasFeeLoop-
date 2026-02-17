import os
import json
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()
w3 = Web3(Web3.HTTPProvider("https://ethereum-sepolia-rpc.publicnode.com"))
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
account = w3.eth.account.from_key(PRIVATE_KEY)

# Címek
REGISTRY = "0x0877298642353805B7c297316A99a2939b541893"
SOVEREIGN = "0x5cf48Be5094bFDaFA647384431f2A513a2979B0E"

# Garantáltan jó, minimális ABI a hatalomátadáshoz
MINIMAL_REGISTRY_ABI = [
    {
        "inputs": [
            {"internalType": "bytes32", "name": "role", "type": "bytes32"},
            {"internalType": "address", "name": "account", "type": "address"}
        ],
        "name": "grantRole",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

# DEFAULT_ADMIN_ROLE konstans (minden 0)
ADMIN_ROLE = "0x0000000000000000000000000000000000000000000000000000000000000000"

registry = w3.eth.contract(address=REGISTRY, abi=MINIMAL_REGISTRY_ABI)

print(f"🚀 Hatalomátadás indítása...")
print(f"🏛️ Registry: {REGISTRY}")
print(f"🛡️ Új Admin (Sovereign): {SOVEREIGN}")

tx = registry.functions.grantRole(ADMIN_ROLE, SOVEREIGN).build_transaction({
    'from': account.address,
    'nonce': w3.eth.get_transaction_count(account.address),
    'gas': 100000,
    'gasPrice': w3.eth.gas_price
})

signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

print(f"⏳ Tranzakció elküldve! Hash: {tx_hash.hex()}")
print("Várjunk a visszaigazolásra...")
receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(f"✅ SIKER! A SovereignModule mostantól a Registry ura.")
