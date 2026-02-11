require('dotenv').config();
const { ethers } = require('ethers');
const fs = require('fs');

async function main() {
    // Contract fájlok
    const abi = JSON.parse(fs.readFileSync('build/HelloCrypto.abi', 'utf8'));
    const bytecode = '0x' + fs.readFileSync('build/HelloCrypto.bin', 'utf8');
    
    // Provider
    const provider = new ethers.JsonRpcProvider(process.env.SEPOLIA_RPC_URL);
    
    // Wallet MNEMONIC-ból (első account)
    const wallet = ethers.Wallet.fromPhrase(process.env.MNEMONIC, provider);
    
    console.log("🔑 Deploying from:", wallet.address);
    
    // Balance check
    const balance = await provider.getBalance(wallet.address);
    console.log("💰 Balance:", ethers.formatEther(balance), "ETH");
    
    // Deploy
    const factory = new ethers.ContractFactory(abi, bytecode, wallet);
    console.log("🚀 Deploying contract...");
    
    const contract = await factory.deploy("Hello from Termux ARM64!");
    await contract.waitForDeployment();
    
    const address = await contract.getAddress();
    console.log("✅ Contract deployed to:", address);
    console.log("🔗 Sepolia Etherscan:", `https://sepolia.etherscan.io/address/${address}`);
}

main().catch(console.error);
