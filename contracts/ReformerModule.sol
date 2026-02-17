// contracts/ReformerModule.sol
import "./IEvolutionaryPath.sol";

abstract contract ReformerModule is IEvolutionaryPath {
    event ReformerPathActivated(address indexed user, uint256 creationId);

    function onPathSelected(EvolutionaryPath path, address user, uint256 amount) external virtual override {
        require(path == EvolutionaryPath.Reformer, "Wrong path");
        // Creative: pl. NFT mint vagy AI prompt trigger (event off-chain-hoz)
        uint256 creationId = block.timestamp; // vagy counter
        emit ReformerPathActivated(user, creationId);
    }
}
