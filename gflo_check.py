import json
from web3 import Web3

w3 = Web3(Web3.HTTPProvider("https://ethereum-sepolia-rpc.publicnode.com"))
SOVEREIGN = "0x5cf48Be5094bFDaFA647384431f2A513a2979B0E"
REGISTRY = "0x0877298642353805B7c297316A99a2939b541893"

with open("gflo_validated.json", "r") as f:
    data = json.load(f)
    # Automatikusan megkeressük a Registry kulcsot
    reg_key = [k for k in data["contracts"].keys() if "UserPathRegistry" in k][0]
    abi = data["contracts"][reg_key]["abi"]

registry = w3.eth.contract(address=REGISTRY, abi=abi)

print(f"🧬 GFLO Validáció...")
print(f"📍 Sovereign: {SOVEREIGN}")
print(f"🏛️ Registry:  {REGISTRY}\n")

try:
    # Ellenőrizzük az alapértelmezett Admin szerepkört
    admin_role = w3.keccak(text="DEFAULT_ADMIN_ROLE").hex()
    is_admin = registry.functions.hasRole(admin_role, SOVEREIGN).call()
    
    print(f"🛡️ Admin jog aktív? {'✅ IGEN' if is_admin else '❌ NEM'}")
    
    if not is_admin:
        print("\n🌱 KÖVETKEZŐ LÉPÉS: Fel kell ruháznunk a Sovereign-t hatalommal.")
        print("Szeretnéd, hogy elkészítsem a 'Grant Role' tranzakciót?")
except Exception as e:
    print(f"❌ Validációs hiba: {e}")
