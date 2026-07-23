// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title GasFeeLoop - Staking & XP Reward System
 * @notice Stake GFLO, earn multiplied XP based on stake amount
 * @dev Integrates with PIECore for XP rewards
 */

interface IERC20 {
    function transferFrom(address from, address to, uint256 amount) external returns (bool);
    function transfer(address to, uint256 amount) external returns (bool);
    function balanceOf(address account) external view returns (uint256);
}

interface IPIECore {
    function addXP(address user, uint256 amount) external;
}

contract GasFeeLoop {
    IERC20 public gfloToken;
    IPIECore public pieCore;
    address public owner;

    struct StakeInfo {
        uint256 amount;
        uint256 timestamp;
        uint256 accumulatedXP;
    }
    mapping(address => StakeInfo) public stakes;

    uint256 public constant EPOCH_DURATION = 7 days;
    uint256 public EPOCH_XP_CAP = 1000 * 10**18;
    mapping(address => mapping(uint256 => uint256)) public epochXP;

    uint256 public baseXPPerTx = 1 * 10**18;
    uint256 public constant MAX_MULTIPLIER = 2 * 10**18;
    uint256 public constant PRECISION = 10**18;

    bool public paused = false;
    uint256 public totalStaked;
    uint256 public totalXPDistributed;

    event Staked(address indexed user, uint256 amount, uint256 newTotal);
    event Unstaked(address indexed user, uint256 amount, uint256 newTotal);
    event XPRewarded(address indexed user, uint256 amount, uint256 multiplier);
    event BaseXPUpdated(uint256 newBase);
    event EpochXPCapUpdated(uint256 newCap);
    event Paused(bool state);

    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }

    modifier notPaused() {
        require(!paused, "Contract paused");
        _;
    }

    constructor(address _gfloToken, address _pieCore) {
        require(_gfloToken != address(0), "Invalid GFLO");
        require(_pieCore != address(0), "Invalid PIECore");

        gfloToken = IERC20(_gfloToken);
        pieCore = IPIECore(_pieCore);
        owner = msg.sender;
    }

    function stake(uint256 amount) external notPaused {
        require(amount > 0, "Amount must be positive");
        require(gfloToken.transferFrom(msg.sender, address(this), amount), "Transfer failed");

        stakes[msg.sender].amount += amount;
        stakes[msg.sender].timestamp = block.timestamp;
        totalStaked += amount;

        emit Staked(msg.sender, amount, stakes[msg.sender].amount);
    }

    function unstake(uint256 amount) external {
        require(amount > 0, "Amount must be positive");
        require(stakes[msg.sender].amount >= amount, "Insufficient stake");

        stakes[msg.sender].amount -= amount;
        totalStaked -= amount;

        require(gfloToken.transfer(msg.sender, amount), "Transfer failed");

        emit Unstaked(msg.sender, amount, stakes[msg.sender].amount);
    }

    function unstakeAll() external {
        uint256 amount = stakes[msg.sender].amount;
        require(amount > 0, "No stake");

        stakes[msg.sender].amount = 0;
        totalStaked -= amount;

        require(gfloToken.transfer(msg.sender, amount), "Transfer failed");

        emit Unstaked(msg.sender, amount, 0);
    }

    function _sqrt(uint256 x) internal pure returns (uint256) {
        if (x == 0) return 0;
        uint256 z = (x + 1) / 2;
        uint256 y = x;
        while (z < y) {
            y = z;
            z = (x / z + z) / 2;
        }
        return y;
    }

    function _calculateMultiplier(address user) internal view returns (uint256) {
        uint256 stakeAmount = stakes[user].amount;
        if (stakeAmount == 0) return PRECISION;

        uint256 s = stakeAmount / PRECISION;
        uint256 m = PRECISION + (_sqrt(s) * PRECISION / 1000);

        return m > MAX_MULTIPLIER ? MAX_MULTIPLIER : m;
    }

    function _addXP(address user, uint256 baseAmount) internal {
        require(stakes[user].amount > 0, "No stake");

        uint256 multiplier = _calculateMultiplier(user);
        uint256 rawXP = (baseAmount * multiplier) / PRECISION;

        uint256 epoch = block.timestamp / EPOCH_DURATION;
        uint256 usedXP = epochXP[user][epoch];

        if (usedXP >= EPOCH_XP_CAP) {
            emit XPRewarded(user, 0, multiplier);
            return;
        }

        uint256 cappedXP = (usedXP + rawXP > EPOCH_XP_CAP) ? EPOCH_XP_CAP - usedXP : rawXP;

        epochXP[user][epoch] += cappedXP;
        stakes[user].accumulatedXP += cappedXP;
        totalXPDistributed += cappedXP;

        pieCore.addXP(user, cappedXP);

        emit XPRewarded(user, cappedXP, multiplier);
    }

    function rewardXP(address user, uint256 amount) external onlyOwner notPaused {
        _addXP(user, amount);
    }

    function batchRewardXP(address[] calldata users, uint256[] calldata amounts) external onlyOwner notPaused {
        require(users.length == amounts.length, "Length mismatch");
        for (uint256 i = 0; i < users.length; i++) {
            if (stakes[users[i]].amount > 0) {
                _addXP(users[i], amounts[i]);
            }
        }
    }

    function getStake(address user) external view returns (uint256) {
        return stakes[user].amount;
    }

    function getMultiplier(address user) external view returns (uint256) {
        return _calculateMultiplier(user);
    }

    function getAccumulatedXP(address user) external view returns (uint256) {
        return stakes[user].accumulatedXP;
    }

    function getEpochXP(address user) external view returns (uint256) {
        uint256 epoch = block.timestamp / EPOCH_DURATION;
        return epochXP[user][epoch];
    }

    function getRemainingEpochXP(address user) external view returns (uint256) {
        uint256 epoch = block.timestamp / EPOCH_DURATION;
        uint256 used = epochXP[user][epoch];
        return used >= EPOCH_XP_CAP ? 0 : EPOCH_XP_CAP - used;
    }

    function getUserInfo(address user) external view returns (
        uint256 stakeAmount,
        uint256 multiplier,
        uint256 accumulatedXP,
        uint256 currentEpochXP,
        uint256 remainingEpochXP
    ) {
        uint256 epoch = block.timestamp / EPOCH_DURATION;
        uint256 usedXP = epochXP[user][epoch];

        return (
            stakes[user].amount,
            _calculateMultiplier(user),
            stakes[user].accumulatedXP,
            usedXP,
            usedXP >= EPOCH_XP_CAP ? 0 : EPOCH_XP_CAP - usedXP
        );
    }

    function setBaseXP(uint256 _baseXP) external onlyOwner {
        require(_baseXP > 0, "Must be positive");
        baseXPPerTx = _baseXP;
        emit BaseXPUpdated(_baseXP);
    }

    function setEpochXPCap(uint256 _cap) external onlyOwner {
        require(_cap > 0, "Must be positive");
        EPOCH_XP_CAP = _cap;
        emit EpochXPCapUpdated(_cap);
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
        gfloToken = IERC20(_gfloToken);
    }
}
