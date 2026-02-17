import os
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()
# Stabilabb RPC végpont használata
w3 = Web3(Web3.HTTPProvider("https://ethereum-sepolia-rpc.publicnode.com"))
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
account = w3.eth.account.from_key(PRIVATE_KEY)

# Hivatalos Registry cím
REGISTRY_ADDR = w3.to_checksum_address("0x0877298642353805B7c297316A99a2939b541893")

ABI = [{"inputs":[{"name":"account","type":"address"}],"name":"getUserPath","outputs":[{"name":"pathName","type":"string"},{"name":"xp","type":"uint256"},{"name":"level","type":"uint256"}],"stateMutability":"view","type":"function"}]

def final_check():
    if not w3.is_connected():
        print("❌ Hiba: Nem sikerült csatlakozni a hálózathoz!")
        return

    contract = w3.eth.contract(address=REGISTRY_ADDR, abi=ABI)
    try:
        data = contract.functions.getUserPath(account.address).call()
        print("\n" + "⭐" * 20)
        print(f"👤 PROFIL: {account.address}")
        print(f"📜 RANG: {data[0]}")
        print(f"✨ XP PONTOK: {data[1]}")
        print(f"🆙 SZINT: {data[2]}")
        print("⭐" * 20 + "\n")
        print("🎉 Minden adat rögzítve! Most már tényleg pihenhetsz.")
    except Exception as e:
        print(f"⚠️ A hálózat még frissül, vagy a cím nem válaszol. Hiba: {e}")

if __name__ == "__main__":
    final_check()
