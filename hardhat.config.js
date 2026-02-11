require("@nomicfoundation/hardhat-toolbox");
require("dotenv").config();

/** @type import('hardhat/config').HardhatUserConfig */
module.exports = {
  solidity: "0.8.20",

  networks: {
    sepolia: {
      url: process.env.SEPOLIA_RPC_URL,
      accounts: {
        mnemonic: process.env.MNEMONIC,
        path: "m/44'/60'/0'/0",
        initialIndex: 1, // <-- ez használja a második accountot (0xBF57...)
        count: 1
      }
    }
  }
};
