// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "./registry/UserPathRegistry.sol";
import "./libraries/MetadataValidator.sol";

contract SovereignModule is Ownable, ReentrancyGuard {
    using MetadataValidator for string;

    UserPathRegistry public immutable pathRegistry;
    address public gfloToken;
    address public treasury;

    uint256 public standardDeployFee = 100 ether;
    uint256 public sovereignDiscount = 50;

    mapping(string => address) public sovWebToToken;

    event MemecoinDeployed(address indexed deployer, address indexed tokenAddress, string sovWeb, bytes32 metadataHash);

    constructor(address _pathRegistry, address _gfloToken, address _treasury) {
        pathRegistry = UserPathRegistry(_pathRegistry);
        gfloToken = _gfloToken;
        treasury = _treasury;
    }

    function deployMemecoin(
        string calldata name, 
        string calldata symbol, 
        string calldata sovWeb, 
        string calldata metadataUri
    ) external nonReentrant returns (address) {
        require(sovWeb.isValidSovWeb(), "Invalid sovWeb");
        require(sovWebToToken[sovWeb] == address(0), "Taken");

        // Kiszámoljuk a díjat közvetlenül a transferben, hogy spóroljunk a stack-kel
        if (standardDeployFee > 0) {
            uint256 fee = (pathRegistry.getUserPath(msg.sender) == UserPathRegistry.UserPath.SOVEREIGN) 
                ? (standardDeployFee * sovereignDiscount) / 100 
                : standardDeployFee;
            IERC20(gfloToken).transferFrom(msg.sender, treasury, fee);
        }

        bytes32 mHash = metadataUri.hashMetadata();
        address mockTokenAddr = address(uint160(uint256(mHash)));
        sovWebToToken[sovWeb] = mockTokenAddr;
        
        pathRegistry.incrementDeployment(msg.sender);
        pathRegistry.awardXP(msg.sender, 10, "Deployed");

        emit MemecoinDeployed(msg.sender, mockTokenAddr, sovWeb, mHash);
        return mockTokenAddr;
    }
}
