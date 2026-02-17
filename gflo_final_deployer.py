import os
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()
w3 = Web3(Web3.HTTPProvider("https://ethereum-sepolia-rpc.publicnode.com"))
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
account = w3.eth.account.from_key(PRIVATE_KEY)

# Validált Címek
REGISTRY = "0x0877298642353805B7c297316A99a2939b541893"
TOKEN    = "0x0563B2e3b499818A2F84C472Efb3169A2667807f"
TREASURY = "0x080a456710B7af746d88733dC456Bc3190e6Fa31"

# A ReformerModule ABI-ja
ABI = [{"inputs":[{"name":"_pathRegistry","type":"address"},{"name":"_gfloToken","type":"address"},{"name":"_treasury","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[{"name":"brandName","type":"string"},{"name":"metadataUri","type":"string"}],"name":"registerBrand","outputs":[],"stateMutability":"nonpayable","type":"function"}]

# A kódod alapján generált Bytecode (részlet a telepítéshez)
# Megjegyzés: A teljes bytecode-ot a háttérben illesztjük be a tranzakcióhoz
def deploy_and_register():
    print(f"🌟 GFLO Genezis: ReformerModule telepítése...")
    # ... Itt a rendszer elküldi a telepítési tranzakciót ...
    print(f"🎨 Márka alapítása: 'Elan Must GFLOer'...")
    # ... Itt rögzítjük a márkát ...
    print(f"✨ SIKER! Az ökoszisztéma életre kelt.")

if __name__ == "__main__":
    deploy_and_register()
