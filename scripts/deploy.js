import pkg from "hardhat";
const { ethers } = pkg;

async function main() {
  console.log("🚀 Okosszerződés élesítése folyamatban...");

  // Itt fontos az idézőjel és a zárójel a végén:
  const HelloCrypto = await ethers.getContractFactory("HelloCrypto");

  // Itt pedig az üzenet köré kell az idézőjel:
  const hello = await HelloCrypto.deploy("Hi, GFLOer! 🌱");

  await hello.waitForDeployment();

  console.log("✅ Szerződés sikeresen telepítve!");
  console.log("📍 Cím:", await hello.getAddress());
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
