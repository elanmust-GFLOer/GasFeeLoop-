// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title GFLOIgnition - Commitment Fuel Layer
 * @notice GFLO Constitution V1 - Phase 2
 * @dev Connects PIECore identity to GFLO burn mechanic.
 *      XP proves merit. GFLO burn proves commitment.
 */

interface IPIECore {
    function isEligibleForUpgrade(address user) external view returns (bool);
    function upgradeTier(address user) external;
    function getIdentity(address user) external view returns (
        uint256 xp,
        uint8 path,
        uint8 tier,
        uint256 nextThreshold
    );
    function setAuthorizedCaller(address caller, bool status) external;
}

interface IGFLOToken {
    function transferFrom(address from, address to, uint256 amount) external returns (bool);
    function burnFrom(address account, uint256 amount) external;
    function burn(uint256 amount) external;
    function balanceOf(address account) external view returns (uint256);
}

contract GFLOIgnition {

    IPIECore public pieCore;
    IGFLOToken public gfloToken;
    address public treasury;
    address public owner;

    mapping(uint8 => uint256) public ignitionCost;
    uint256 public burnRatio = 50;
    uint256 public treasuryRatio = 50;
    bool public paused = false;

    uint256 public totalBurned;
    uint256 public totalIgnitions;

    event Ignited(address indexed user, uint8 newTier, uint256 burned, uint256 toTreasury);
    event IgnitionCostSet(uint8 tier, uint256 cost);
    event TreasuryUpdated(address newTreasury);
    event Paused(bool state);
    event BurnRatioUpdated(uint256 burnRatio, uint256 treasuryRatio);

    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }

    modifier notPaused() {
        require(!paused, "Contract paused");
        _;
    }

    constructor(address _pieCore, address _gfloToken, address _treasury) {
        require(_pieCore != address(0), "Invalid PIECore");
        require(_gfloToken != address(0), "Invalid GFLO");
        require(_treasury != address(0), "Invalid treasury");

        owner = msg.sender;
        pieCore = IPIECore(_pieCore);
        gfloToken = IGFLOToken(_gfloToken);
        treasury = _treasury;

        ignitionCost[0] = 100 * 10**18;
        ignitionCost[1] = 500 * 10**18;
        ignitionCost[2] = 2000 * 10**18;

        pieCore.setAuthorizedCaller(address(this), true);
    }

    /**
     * @notice Ignite upgrade - burn GFLO to advance tier
     */
    function igniteUpgrade() external notPaused {
        require(pieCore.isEligibleForUpgrade(msg.sender), "Not eligible: insufficient XP");

        (uint256 xp, uint8 path, uint8 currentTier, uint256 nextThreshold) = pieCore.getIdentity(msg.sender);
        require(currentTier < 3, "Max tier reached");
        require(xp >= nextThreshold, "Insufficient XP");

        uint256 cost = ignitionCost[currentTier];
        require(cost > 0, "Ignition cost not set");
        require(gfloToken.balanceOf(msg.sender) >= cost, "Insufficient GFLO");

        uint256 toBurn = (cost * burnRatio) / 100;
        uint256 toTreasury = cost - toBurn;

        require(gfloToken.transferFrom(msg.sender, address(this), cost), "Transfer failed");

        gfloToken.burn(toBurn);
        if (toTreasury > 0) {
            try gfloToken.transferFrom(address(this), treasury, toTreasury) {
            } catch {
                gfloToken.burn(toTreasury);
            }
        }

        pieCore.upgradeTier(msg.sender);

        totalBurned += cost;
        totalIgnitions++;

        emit Ignited(msg.sender, currentTier + 1, toBurn, toTreasury);
    }

    function getIgnitionCost(address user) external view returns (uint256 cost, bool canAfford, bool xpEligible) {
        (, , uint8 tier, ) = pieCore.getIdentity(user);
        cost = ignitionCost[tier];
        canAfford = gfloToken.balanceOf(user) >= cost;
        xpEligible = pieCore.isEligibleForUpgrade(user);
    }

    function isReadyToIgnite(address user) external view returns (bool) {
        (, , uint8 tier, ) = pieCore.getIdentity(user);
        if (tier >= 3) return false;
        uint256 cost = ignitionCost[tier];
        return pieCore.isEligibleForUpgrade(user) && gfloToken.balanceOf(user) >= cost;
    }

    function setIgnitionCost(uint8 tier, uint256 cost) external onlyOwner {
        require(cost > 0, "Cost must be positive");
        ignitionCost[tier] = cost;
        emit IgnitionCostSet(tier, cost);
    }

    function setTreasury(address _treasury) external onlyOwner {
        require(_treasury != address(0), "Invalid treasury");
        treasury = _treasury;
        emit TreasuryUpdated(_treasury);
    }

    function setBurnRatio(uint256 _burnRatio) external onlyOwner {
        require(_burnRatio <= 100, "Invalid ratio");
        burnRatio = _burnRatio;
        treasuryRatio = 100 - _burnRatio;
        emit BurnRatioUpdated(_burnRatio, treasuryRatio);
    }

    function setPaused(bool _paused) external onlyOwner {
        paused = _paused;
        emit Paused(_paused);
    }

    function setPieCore(address _pieCore) external onlyOwner {
        require(_pieCore != address(0), "Invalid PIECore");
        pieCore = IPIECore(_pieCore);
    }

    function setGfloToken(address _gfloToken) external onlyOwner {
        require(_gfloToken != address(0), "Invalid GFLO");
        gfloToken = IGFLOToken(_gfloToken);
    }
}
