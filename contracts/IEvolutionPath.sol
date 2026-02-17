// contracts/IEvolutionaryPath.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

enum EvolutionaryPath {
    Sovereign,  // 0: Entry-level autonomy – simple onboarding, memecoin deployment
    Praxis,     // 1: Open building tools – developer/mentor feature-ök (pl. audit log, code hints)
    Reformer    // 2: Creative transformation – NFT/AI/generative (pl. extra mint vagy event)
}

interface IEvolutionaryPath {
    function onPathSelected(EvolutionaryPath path, address user, uint256 amount) external;
    // Opcionális: extra gas-efficient hook-ok
}
