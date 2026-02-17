import os
import json
from web3 import Web3
from solcx import compile_source, install_solc
from dotenv import load_dotenv

load_dotenv()

# 1. Solidity verzió telepítése
install_solc('0.8.20')

# 2. Szerződés forráskódja (beolvassuk a fájlból)
with open('UserPathRegistry.sol', 'r') as f:
    source_code = f.read()

# 3. Fordítás
compiled_sol = compile_source(
    source_code,
    output_values=['abi', 'bin'],
    solc_version='0.8.20'
)

# Kinyerjük az ABI-t és a Bytecode-ot
contract_id, contract_interface = compiled_sol.popitem()
abi = contract_interface['abi']
bytecode = contract_interface['bin']

# Mentsük el az ABI-t, hogy később az app.py tudja használni!
with open('UserPathRegistry_abi.json', 'w') as f:
    json.dump(abi, f)

# 4. Csatlakozás és Deploy
w3 = Web3(Web3.HTTPProvider(os.getenv("SEPOLIA_RPC_URL")))
private_key = os.getenv("PRIVATE_KEY")
account = w3.eth.account.from_key(private_key)

print("🚀 Szerződés feltöltése indul...")

# Tranzakció építése
RegistryContract = w3.eth.contract(abi=abi, bytecode=bytecode)
construct_txn = RegistryContract.constructor().build_transaction({
    'from': account.address,
    'nonce': w3.eth.get_transaction_count(account.address),
    'gasPrice': w3.eth.gas_price
})

# Aláírás és küldés
signed_tx = w3.eth.account.sign_transaction(construct_txn, private_key)
tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

print(f"✅ SIKER! A szerződés címe: {tx_receipt.contractAddress}")
