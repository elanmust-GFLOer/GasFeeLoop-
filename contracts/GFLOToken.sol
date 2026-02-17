// contracts/GFLOToken.sol
import "./SovereignModule.sol";
import "./PraxisModule.sol";
import "./ReformerModule.sol";
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract GFLOToken is ERC20, SovereignModule, PraxisModule, ReformerModule {
    constructor() ERC20("GFLO", "GFLO") {
        _mint(msg.sender, 1_000_000_000 * 10**decimals());
    }

    // Extended transfer path választással
    function transferWithPath(address to, uint256 amount, EvolutionaryPath path) public returns (bool) {
        _transfer(msg.sender, to, amount);
        // Path hook – itt hívódnak a modulok (gas-optimal: csak a választott fut)
        if (path == EvolutionaryPath.Sovereign) {
            SovereignModule.onPathSelected(path, msg.sender, amount);
        } else if (path == EvolutionaryPath.Praxis) {
            PraxisModule.onPathSelected(path, msg.sender, amount);
        } else if (path == EvolutionaryPath.Reformer) {
            ReformerModule.onPathSelected(path, msg.sender, amount);
        }
        return true;
    }

    // Normál transfer fallback (default Sovereign)
    function transfer(address to, uint256 amount) public override returns (bool) {
        return transferWithPath(to, amount, EvolutionaryPath.Sovereign);
    }
}
