require("dotenv").config(); // Kisbetűs require!
const { ethers } = require("ethers");
const fs = require("fs");

async function main() {
    // 1. Kapcsolódás az Infurához
    const provider = new ethers.providers.JsonRpcProvider(process.env.SEPOLIA_RPC_URL);

    // 2. Tárca létrehozása
    const mnemonic = process.env.MNEMONIC;
    if (!mnemonic) {
        throw new Error("A MNEMONIC hiányzik a .env fájlból!");
    }

    const wallet = ethers.Wallet.fromMnemonic(mnemonic).connect(provider);
    console.log("🚀 Deploy indítása a következő tárcával:", wallet.address);

    // 3. JSON beolvasása
    const contractPath = "./artifacts/contracts/HelloCrypto.sol/HelloCrypto.json";
    const contractJson = JSON.parse(fs.readFileSync(contractPath, "utf8"));
    const abi = contractJson.abi;
    const bytecode = contractJson.bytecode;

    // 4. Szerződés gyár
    const factory = new ethers.ContractFactory(abi, bytecode, wallet);

    console.log("⏳ Tranzakció küldése a Sepolia hálózatra...");
    
    // ITT ADJUK ÁT AZ INITIAL MESSAGE-T!
    const contract = await factory.deploy("Szia a blokklancrol!"); 

    console.log("🔗 Tranzakció hash:", contract.deployTransaction.hash);

    console.log("⌛ Várakozás a visszaigazolásra...");
    await contract.deployed();

    console.log("✅ SIKER! A szerződés címe:", contract.address);
}

main().catch((error) => {
    console.error("❌ Hiba történt:", error);
    process.exit(1);
});
