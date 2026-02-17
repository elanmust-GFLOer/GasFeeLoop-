import os
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()
w3 = Web3(Web3.HTTPProvider("https://ethereum-sepolia-rpc.publicnode.com"))
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
account = w3.eth.account.from_key(PRIVATE_KEY)

# Registry címe
REGISTRY_ADDR = "0x0877298642353805B7c297316A99a2939b541893"

# Minimális ABI a lekérdezéshez
ABI = [
    {"inputs": [{"name": "account", "type": "address"}], "name": "getUserPath", "outputs": [{"name": "pathName", "type": "string"}, {"name": "xp", "type": "uint256"}, {"name": "level", "type": "uint256"}], "stateMutability": "view", "type": "function"}
]

def check():
    contract = w3.eth.contract(address=REGISTRY_ADDR, abi=ABI)
    user_data = contract.functions.getUserPath(account.address).call()
    
    print("\n" + "="*30)
    print(f"🏆 GFLOER PROFIL: {account.address[:10]}...")
    print(f"✨ Útvonal (Rang): {user_data[0]}")
    print(f"📈 Összes XP: {user_data[1]}")
    print(f"🆙 Szint: {user_data[2]}")
    print("="*30 + "\n")
    print("Gratulálok! Az 'Elan Must GFLOer' márka alapköveit letetted. 💤")

if __name__ == "__main__":
    check()
