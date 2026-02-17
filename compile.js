const solc = require('solc');
const fs = require('fs');
const path = require('path');

// Olvasd be a szerződés forrását
const contractPath = path.join(__dirname, 'contracts', 'GFLOToken.sol'); // Válaszd ki a fő szerződésed
const source = fs.readFileSync(contractPath, 'utf8');

// Fordítási bemenet
const input = {
  language: 'Solidity',
  sources: {
    'GFLOToken.sol': {
      content: source
    }
  },
  settings: {
    outputSelection: {
      '*': {
        '*': ['*']
      }
    }
  }
};

const output = JSON.parse(solc.compile(JSON.stringify(input)));

// Hibakezelés
if (output.errors) {
  output.errors.forEach(err => console.error(err.formattedMessage));
}

// ABI és Bytecode mentése
for (const contractName in output.contracts['GFLOToken.sol']) {
  const artifact = {
    abi: output.contracts['GFLOToken.sol'][contractName].abi,
    bytecode: output.contracts['GFLOToken.sol'][contractName].evm.bytecode.object
  };
  fs.writeFileSync(
    path.join(__dirname, 'artifacts', `${contractName}.json`),
    JSON.stringify(artifact, null, 2)
  );
  console.log(`✅ ${contractName} lefordítva és elmentve.`);
}
