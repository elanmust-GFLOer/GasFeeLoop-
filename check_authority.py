import json
from web3 import Web3

w3 = Web3(Web3.HTTPProvider("https://ethereum-sepolia-rpc.publicnode.com"))
SOVEREIGN = "0x5cf48Be5094bFDaFA647384431f2A513a2979B0E"
REGISTRY = "0x0877298642353805B7c297316A99a2939b541893"

# Beolvassuk a Registry ABI-t (UserPathRegistry.sol-ból fordítva)
with open("compiled.json", "r") as f:
    data = json.load(f)
    # Keressük meg a Registry ABI-ját
    abi = data["contracts"]["UserPathRegistry.sol:UserPathRegistry"]["abi"]

registry_contract = w3.eth.contract(address=REGISTRY, abi=abi)

def check():
    print(f"🕵️ GFLO Rendszer Validáció: Jogosultságok ellenőrzése...")
    
    # A DEFAULT_ADMIN_ROLE hash-e (standard OpenZeppelin)
    ADMIN_ROLE = "0x0000000000000000000000000000000000000000000000000000000000000000"
    
    try:
        has_role = registry_contract.functions.hasRole(ADMIN_ROLE, SOVEREIGN).call()
        print(f"\n🔑 SovereignModule ADMIN_ROLE státusz: {'✅ IGEN' if has_role else '❌ NEM'}")
        
        if not has_role:
            print("\n💡 Megjegyzés: A SovereignModule telepítve van, de még nem kapott hatalmat a Registry felett.")
            print("Ezt a 'grantRole' függvénnyel kell majd orvosolnunk a Registry-ben.")
        else:
            print("\n🚀 A Rendszer AKTÍV: A SovereignModule irányíthatja a Registry-t!")
            
    except Exception as e:
        print(f"❌ Hiba a lekérdezéskor: {e}")

if __name__ == "__main__":
    check()
