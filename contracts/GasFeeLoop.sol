// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface IERC20 {
    function transferFrom(address from, address to, uint256 amount) external returns (bool);
    function transfer(address to, uint256 amount) external returns (bool);
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
    uint256 public constant EPOCH_XP_CAP = 1000 * 10**18;
    mapping(address => mapping(uint256 => uint256)) public epochXP;

    uint256 public baseXPPerTx = 1 * 10**18;
    uint256 public constant MAX_MULTIPLIER = 2 * 10**18;
    uint256 public constant PRECISION = 10**18;

    event Staked(address indexed user, uint256 amount);
    event Unstaked(address indexed user, uint256 amount);
    event XPRewarded(address indexed user, uint256 amount);

    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }

    constructor(address _gfloToken, address _pieCore) {
        gfloToken = IERC20(_gfloToken);
        pieCore = IPIECore(_pieCore);
        owner = msg.sender;
    }

    function stake(uint256 amount) external {
        require(amount > 0, "Amount must be positive");
        require(gfloToken.transferFrom(msg.sender, address(this), amount), "Transfer failed");
        stakes[msg.sender].amount += amount;
        stakes[msg.sender].timestamp = block.timestamp;
        emit Staked(msg.sender, amount);
    }

    function unstake(uint256 amount) external {
        require(amount > 0, "Amount must be positive");
        require(stakes[msg.sender].amount >= amount, "Insufficient stake");
        stakes[msg.sender].amount -= amount;
        require(gfloToken.transfer(msg.sender, amount), "Transfer failed");
        emit Unstaked(msg.sender, amount);
    }

    function _sqrt(uint256 x) internal pure returns (uint256) {
        if (x == 0) return 0;
        uint256 z = (x + 1) / 2;
        uint256 y = x;
        while (z < y) { y = z; z = (x / z + z) / 2; }
        return y;
    }

    function _calculateMultiplier(address user) internal view returns (uint256) {
        uint256 s = stakes[user].amount / PRECISION;
        if (s == 0) return PRECISION;
        uint256 m = PRECISION + (_sqrt(s) * PRECISION / 1000);
        return m > MAX_MULTIPLIER ? MAX_MULTIPLIER : m;
    }

    function _addXP(address user, uint256 baseAmount) internal {
        uint256 multiplier = _calculateMultiplier(user);
        uint256 rawXP = baseAmount * multiplier / PRECISION;
        uint256 epoch = block.timestamp / EPOCH_DURATION;
        uint256 used = epochXP[user][epoch];
        if (used >= EPOCH_XP_CAP) return;
        uint256 capped = (used + rawXP > EPOCH_XP_CAP) ? EPOCH_XP_CAP - used : rawXP;
        epochXP[user][epoch] += capped;
        stakes[user].accumulatedXP += capped;
        pieCore.addXP(user, capped);
        emit XPRewarded(user, capped);
    }

    function rewardXP(address user, uint256 amount) external onlyOwner {
        _addXP(user, amount);
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
}
