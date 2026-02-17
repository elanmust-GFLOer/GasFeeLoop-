import json
import os
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

# A frissen telepített modulod címe
CONTRACT_ADDRESS = "0x5cf48Be5094bFDaFA647384431f2A513a2979B0E"
RPC_URL = "https://ethereum-sepolia-rpc.publicnode.com"

def verify():
    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    
    if not w3.is_connected():
        print("❌ Nem sikerült csatlakozni az RPC-hez!")
        return

    # ABI betöltése
    try:
        with open("compiled_sovereign.json", "r") as f:
            data = json.load(f)
        abi = data["contracts"]["SovereignModule.sol:SovereignModule"]["abi"]
    except Exception as e:
        print(f"❌ ABI betöltési hiba: {e}")
        return

    contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)

    print(f"🔍 Szerződés ellenőrzése: {CONTRACT_ADDRESS}\n")
    
    try:
        # Lekérdezzük a változókat a blokkláncról
        # Megjegyzés: Ha a .sol fájlban 'registry' néven van a változó, a web3 automatikusan generál hozzá egy getter függvényt
        reg = contract.functions.registry().call()
        tok = contract.functions.token().call()
        tre = contract.functions.treasury().call()

        print(f"🏢 Registry: {reg}")
        print(f"🪙 Token:    {tok}")
        print(f"💰 Treasury: {tre}")
        
        print("\n✅ Ha ezek a címek egyeznek az eredetileg megadottakkal, a rendszer tökéletes!")
    except Exception as e:
        print(f"❌ Hiba a lekérdezéskor: {e}")
        print("Tipp: Ellenőrizd a .sol fájlban a változók nevét (lehet, hogy _registry vagy hasonló)!")

if __name__ == "__main__":
    verify()
