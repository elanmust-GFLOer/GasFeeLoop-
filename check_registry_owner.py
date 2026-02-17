import json
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()
w3 = Web3(Web3.HTTPProvider("https://ethereum-sepolia-rpc.publicnode.com"))
REGISTRY = "0x0877298642353805B7c297316A99a2939b541893"
SOVEREIGN = "0x5cf48Be5094bFDaFA647384431f2A513a2979B0E"

with open("compiled.json", "r") as f:
    data = json.load(f)
    abi = data["contracts"]["UserPathRegistry.sol:UserPathRegistry"]["abi"]

registry = w3.eth.contract(address=REGISTRY, abi=abi)
ADMIN_ROLE = "0x0000000000000000000000000000000000000000000000000000000000000000"

def check():
    owner = w3.eth.account.from_key(os.getenv("PRIVATE_KEY")).address
    print(f"🕵️ Saját címed: {owner}")
    print(f"🏛️ Registry: {REGISTRY}")
    
    is_owner_admin = registry.functions.hasRole(ADMIN_ROLE, owner).call()
    is_sov_admin = registry.functions.hasRole(ADMIN_ROLE, SOVEREIGN).call()
    
    print(f"\n🔑 Te vagy az admin? {'✅ IGEN' if is_owner_admin else '❌ NEM'}")
    print(f"🛡️ SovereignModule admin? {'✅ IGEN' if is_sov_admin else '❌ NEM'}")

if __name__ == "__main__":
    check()
