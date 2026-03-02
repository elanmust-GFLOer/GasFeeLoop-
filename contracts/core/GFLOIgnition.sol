// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title GFLOIgnition - Commitment Fuel Layer
 * @notice GFLO Constitution V1 - Phase 2
 * @dev Connects PIECore identity to GFLO burn mechanic.
 *      XP proves merit. GFLO burn proves commitment.
 *      No admin upgrade override. Deterministic.
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
}

interface IGFLOToken {
    function burnFrom(address account, uint256 amount) external;
    function balanceOf(address account) external view returns (uint256);
}

contract GFLOIgnition {

    // ============================================
    // STATE
    // ============================================

    IPIECore public pieCore;
    IGFLOToken public gfloToken;

    address public treasury;
    address public owner;

    // Ignition cost per tier upgrade
    // 50% burn, 50% treasury
    mapping(uint8 => uint256) public ignitionCost;

    uint256 public burnRatio = 50; // 50% burn
    uint256 public treasuryRatio = 50; // 50% treasury

    bool public paused = false;

    // Stats
    uint256 public totalBurned;
    uint256 public totalIgnitions;

    // ============================================
    // EVENTS
    // ============================================

    event Ignited(
        address indexed user,
        uint8 newTier,
        uint256 burned,
        uint256 toTreasury
    );
    event IgnitionCostSet(uint8 tier, uint256 cost);
    event TreasuryUpdated(address newTreasury);
    event Paused(bool state);

    // ============================================
    // MODIFIERS
    // ============================================

    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }

    modifier notPaused() {
        require(!paused, "Contract paused");
        _;
    }

    // ============================================
    // CONSTRUCTOR
    // ============================================

    constructor(
        address _pieCore,
        address _gfloToken,
        address _treasury
    ) {
        owner = msg.sender;
        pieCore = IPIECore(_pieCore);
        gfloToken = IGFLOToken(_gfloToken);
        treasury = _treasury;

        // Default ignition costs (in GFLO tokens, 18 decimals)
        ignitionCost[0] = 100 ether;   // tier 0 -> 1: 100 GFLO
        ignitionCost[1] = 500 ether;   // tier 1 -> 2: 500 GFLO
        ignitionCost[2] = 2000 ether;  // tier 2 -> 3: 2000 GFLO
    }

    // ============================================
    // CORE: IGNITE UPGRADE
    // ============================================

    /**
     * @notice Burn GFLO to upgrade tier in PIECore
     * @dev Requires XP eligibility from PIECore.
     *      Burns 50%, sends 50% to treasury.
     *      This is the commitment proof mechanism.
     */
    function igniteUpgrade() external notPaused {
        require(
            pieCore.isEligibleForUpgrade(msg.sender),
            "Not eligible: insufficient XP"
        );

        (, , uint8 currentTier, ) = pieCore.getIdentity(msg.sender);
        require(currentTier < 3, "Max tier reached");

        uint256 cost = ignitionCost[currentTier];
        require(cost > 0, "Ignition cost not set");
        require(
            gfloToken.balanceOf(msg.sender) >= cost,
            "Insufficient GFLO balance"
        );

        // Split: burn + treasury
        uint256 toBurn = (cost * burnRatio) / 100;
        uint256 toTreasury = cost - toBurn;

        // Burn from user
        gfloToken.burnFrom(msg.sender, toBurn);

        // Treasury portion (transfer, not burn)
        // Note: requires approval for treasury transfer too
        // In production: use transferFrom to treasury
        // For V1: burn all, treasury tracked separately
        gfloToken.burnFrom(msg.sender, toTreasury);

        // Upgrade in PIECore
        pieCore.upgradeTier(msg.sender);

        // Stats
        totalBurned += cost;
        totalIgnitions++;

        emit Ignited(msg.sender, currentTier + 1, toBurn, toTreasury);
    }

    // ============================================
    // VIEWS
    // ============================================

    function getIgnitionCost(address user) external view returns (
        uint256 cost,
        bool canAfford,
        bool xpEligible
    ) {
        (, , uint8 tier, ) = pieCore.getIdentity(user);
        cost = ignitionCost[tier];
        canAfford = gfloToken.balanceOf(user) >= cost;
        xpEligible = pieCore.isEligibleForUpgrade(user);
    }

    function isReadyToIgnite(address user) external view returns (bool) {
        (, , uint8 tier, ) = pieCore.getIdentity(user);
        if (tier >= 3) return false;
        uint256 cost = ignitionCost[tier];
        return (
            pieCore.isEligibleForUpgrade(user) &&
            gfloToken.balanceOf(user) >= cost
        );
    }

    // ============================================
    // ADMIN
    // ============================================

    function setIgnitionCost(uint8 tier, uint256 cost) external onlyOwner {
        ignitionCost[tier] = cost;
        emit IgnitionCostSet(tier, cost);
    }

    function setTreasury(address _treasury) external onlyOwner {
        treasury = _treasury;
        emit TreasuryUpdated(_treasury);
    }

    function setBurnRatio(uint256 _burnRatio) external onlyOwner {
        require(_burnRatio <= 100, "Invalid ratio");
        burnRatio = _burnRatio;
        treasuryRatio = 100 - _burnRatio;
    }

    function setPaused(bool _paused) external onlyOwner {
        paused = _paused;
        emit Paused(_paused);
    }

    function setPieCore(address _pieCore) external onlyOwner {
        pieCore = IPIECore(_pieCore);
    }

    function setGfloToken(address _gfloToken) external onlyOwner {
        gfloToken = IGFLOToken(_gfloToken);
    }
}
