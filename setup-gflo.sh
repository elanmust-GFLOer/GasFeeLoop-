#!/bin/bash
set -e

echo "🚀 GFLO Hardhat Environment Setup (Ubuntu/WSL/Debian) 🚀"

# 1️⃣ Rendszer frissítés és alap eszközök
sudo apt update && sudo apt upgrade -y
sudo apt install -y build-essential curl git unzip

# 2️⃣ Node.js 20 LTS telepítés
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs

echo "✅ Node.js és npm telepítve"
node -v
npm -v

# 3️⃣ Projekt könyvtár létrehozása
PROJECT_DIR="$HOME/gflo-pie"
mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"
echo "✅ Projekt könyvtár létrehozva: $PROJECT_DIR"

# 4️⃣ Hardhat telepítése
npm init -y
npm install --save-dev hardhat
npx hardhat init --force
echo "✅ Hardhat telepítve és inicializálva"

# 5️⃣ Toolbox + Ignition telepítése
npm install --save-dev @nomicfoundation/hardhat-toolbox
npm install --save-dev @nomicfoundation/hardhat-ignition
npm install --save-dev @nomicfoundation/hardhat-ignition-ethers
npm install --save-dev @nomicfoundation/hardhat-ethers ethers

echo "✅ Hardhat Toolbox + Ignition + Ethers telepítve"

# 6️⃣ Példa .env fájl
cat <<EOL > .env
MNEMONIC="több szavas mnemonikod ide"
INFURA_KEY="ide_az_infura_key"
EOL
echo "✅ .env fájl létrehozva"

# 7️⃣ Hardhat konfiguráció
cat <<EOL > hardhat.config.js
require("@nomicfoundation/hardhat-toolbox");
require("@nomicfoundation/hardhat-ignition");

module.exports = {
  solidity: "0.8.20",
  defaultNetwork: "sepolia",
  networks: {
    sepolia: {
      url: "https://sepolia.infura.io/v3/" + process.env.INFURA_KEY,
      accounts: { mnemonic: process.env.MNEMONIC }
    }
  }
};
EOL
echo "✅ Hardhat config kész"

# 8️⃣ Mintascript könyvtár és példa deploy.js
mkdir -p scripts contracts
cat <<EOL > scripts/deploy.js
async function main() {
  const [deployer] = await ethers.getSigners();
  console.log("Deploying contracts with account:", deployer.address);

  const UserPathRegistry = await ethers.getContractFactory("UserPathRegistry");
  const contract = await UserPathRegistry.deploy();
  await contract.deployed();

  console.log("UserPathRegistry deployed to:", contract.address);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
EOL
echo "✅ Deploy script kész"

echo "🎉 Setup kész! Lépj be a projekt könyvtárba: cd $PROJECT_DIR"
echo "npx hardhat compile"
echo "npx hardhat run scripts/deploy.js --network sepolia"
