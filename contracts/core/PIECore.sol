// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface IGFLO {
    function transferFrom(address from, address to, uint256 amount) external returns (bool);
    function burnFrom(address account, uint256 amount) external;
    function burn(uint256 amount) external;
    function balanceOf(address account) external view returns (uint256);
}

/**
 * @title PIECore - Path Identity Engine (GasFeeLoop version)
 * @notice Compatible with GFLOIgnition and GasFeeLoop
 */
contract PIECore {
    enum Path { None, Sovereign, Reformer, Praxis }

    struct Identity {
        uint256 xp;
        Path path;
        uint8 tier;
    }

    mapping(address => Identity) public identities;
    IGFLO public gfloToken;

    uint256 public constant SOVEREIGN_TIER1_XP = 1000;
    uint256 public constant REFORMER_BURN_AMOUNT = 5000 * 10**18;
    uint256 public constant PRAXIS_BURN_AMOUNT = 10000 * 10**18;

    event PathChosen(address indexed user, Path path);
    event XPGained(address indexed user, uint256 amount);
    event TierUpgraded(address indexed user, uint8 newTier);
    event CommitmentBurned(address indexed user, uint256 amount);

    constructor(address _gfloAddress) {
        gfloToken = IGFLO(_gfloAddress);
    }

    function choosePath(Path _path) external {
        require(_path != Path.None, "Invalid path");
        require(identities[msg.sender].path == Path.None, "Already chosen");

        identities[msg.sender].path = _path;
        identities[msg.sender].tier = 0;
        identities[msg.sender].xp = 0;

        emit PathChosen(msg.sender, _path);
    }

    function gainXP(uint256 amount) external {
        require(identities[msg.sender].path != Path.None, "Choose path first");
        identities[msg.sender].xp += amount;
        emit XPGained(msg.sender, amount);
    }

    function addXP(address user, uint256 amount) external {
        require(identities[user].path != Path.None, "User has no path");
        identities[user].xp += amount;
        emit XPGained(user, amount);
    }

    function upgradeToReformer() external {
        Identity storage user = identities[msg.sender];
        require(user.path == Path.Sovereign, "Must be Sovereign first");
        require(user.xp >= SOVEREIGN_TIER1_XP, "Insufficient XP");

        require(gfloToken.transferFrom(msg.sender, address(this), REFORMER_BURN_AMOUNT), "Transfer failed");
        gfloToken.burn(REFORMER_BURN_AMOUNT);

        user.path = Path.Reformer;
        user.tier = 1;

        emit CommitmentBurned(msg.sender, REFORMER_BURN_AMOUNT);
        emit TierUpgraded(msg.sender, 1);
        emit PathChosen(msg.sender, Path.Reformer);
    }

    function upgradeToPraxis() external {
        Identity storage user = identities[msg.sender];
        require(user.path == Path.Reformer, "Must be Reformer first");
        require(user.xp >= 5000, "Insufficient XP");

        require(gfloToken.transferFrom(msg.sender, address(this), PRAXIS_BURN_AMOUNT), "Transfer failed");
        gfloToken.burn(PRAXIS_BURN_AMOUNT);

        user.path = Path.Praxis;
        user.tier = 2;

        emit CommitmentBurned(msg.sender, PRAXIS_BURN_AMOUNT);
        emit TierUpgraded(msg.sender, 2);
        emit PathChosen(msg.sender, Path.Praxis);
    }

    function getIdentity(address user) external view returns (
        uint256 xp,
        uint8 path,
        uint8 tier,
        uint256 nextThreshold
    ) {
        Identity memory id = identities[user];
        uint8 pathUint = uint8(id.path);
        uint256 threshold = 0;

        if (id.path == Path.Sovereign) {
            threshold = SOVEREIGN_TIER1_XP;
        } else if (id.path == Path.Reformer) {
            threshold = 5000;
        }

        return (id.xp, pathUint, id.tier, threshold);
    }

    function getXP(address user) external view returns (uint256) {
        return identities[user].xp;
    }

    function getTier(address user) external view returns (uint8) {
        return identities[user].tier;
    }

    function getPath(address user) external view returns (Path) {
        return identities[user].path;
    }

    function isEligibleForUpgrade(address user) external view returns (bool) {
        Identity memory id = identities[user];
        if (id.path == Path.Sovereign) {
            return id.xp >= SOVEREIGN_TIER1_XP;
        } else if (id.path == Path.Reformer) {
            return id.xp >= 5000;
        }
        return false;
    }

    function upgradeTier(address user) external {
        Identity storage id = identities[user];
        require(id.path != Path.None, "User has no path");

        if (id.path == Path.Sovereign) {
            require(id.xp >= SOVEREIGN_TIER1_XP, "Insufficient XP");
            id.path = Path.Reformer;
            id.tier = 1;
            emit TierUpgraded(user, 1);
            emit PathChosen(user, Path.Reformer);
        } else if (id.path == Path.Reformer) {
            require(id.xp >= 5000, "Insufficient XP");
            id.path = Path.Praxis;
            id.tier = 2;
            emit TierUpgraded(user, 2);
            emit PathChosen(user, Path.Praxis);
        } else {
            revert("Already at max tier");
        }
    }
}
