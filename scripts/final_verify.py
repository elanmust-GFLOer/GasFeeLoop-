import json
from web3 import Web3

w3 = Web3(Web3.HTTPProvider("https://ethereum-sepolia-rpc.publicnode.com"))
addr = "0x5cf48Be5094bFDaFA647384431f2A513a2979B0E"

with open("compiled_sovereign.json", "r") as f:
    abi = json.load(f)["contracts"]["SovereignModule.sol:SovereignModule"]["abi"]

contract = w3.eth.contract(address=addr, abi=abi)

def try_call(names):
    for name in names:
        try:
            return getattr(contract.functions, name)().call(), name
        except:
            continue
    return None, "Not Found"

print(f"📡 Kapcsolódás: {addr}\n")

# Próbáljuk meg mindkét verziót (alulvonással és anélkül)
reg_val, reg_name = try_call(["pathRegistry", "_pathRegistry"])
tok_val, tok_name = try_call(["gfloToken", "_gfloToken"])
tre_val, tre_name = try_call(["treasury", "_treasury"])

print(f"🏢 Registry ({reg_name}): {reg_val}")
print(f"🪙 Token ({tok_name}):    {tok_val}")
print(f"💰 Treasury ({tre_name}): {tre_val}")

if reg_val and tok_val and tre_val:
    print("\n✅ SIKER! A szellemek végleg elűzve, a kapcsolatok élnek.")
else:
    print("\n⚠️ Valamelyik címet még mindig rejtegeti a szerződés.")
