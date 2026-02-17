// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/AccessControl.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

/**
 * @title UserPathRegistry
 * @notice Core registry for GFLO Sovereign path selection system
 * @dev Tracks user paths (SOVEREIGN, PRAXIS, REFORMER) and manages path switching
 * @custom:security-contact security@gflo.vision
 */
contract UserPathRegistry is AccessControl, ReentrancyGuard {
    // =============================================================
    //                          CONSTANTS
    // =============================================================

    bytes32 public constant ADMIN_ROLE = keccak256("ADMIN_ROLE");
    bytes32 public constant MODULE_ROLE = keccak256("MODULE_ROLE");

    uint256 public constant PATH_SWITCH_COOLDOWN = 30 days;
    uint256 public constant MIN_XP_FOR_SWITCH = 100; // Prevent spam switching

    // =============================================================
    //                           ENUMS
    // =============================================================

    enum UserPath {
        NONE,       // 0 - Not chosen yet
        SOVEREIGN,  // 1 - Entry level (basic deploy)
        PRAXIS,     // 2 - Developer/Mentor path
        REFORMER    // 3 - Creator/Artist path
    }

    // =============================================================
    //                          STRUCTS
    // =============================================================

    struct UserProfile {
        UserPath currentPath;
        uint256 pathChosenAt;
        uint256 lastPathSwitchAt;
        uint256 xpBalance;
        uint256 totalDeployments;
        bool isActive;
    }

    // =============================================================
    //                          STORAGE
    // =============================================================

    mapping(address => UserProfile) public users;
    mapping(UserPath => uint256) public pathCounts; // Track distribution

    uint256 public totalUsers;

    // =============================================================
    //                          EVENTS
    // =============================================================

    event PathChosen(
        address indexed user,
        UserPath indexed path,
        uint256 timestamp
    );

    event PathSwitched(
        address indexed user,
        UserPath indexed fromPath,
        UserPath indexed toPath,
        uint256 timestamp
    );

    event XPAwarded(
        address indexed user,
        uint256 amount,
        string reason
    );

    event UserDeactivated(address indexed user, uint256 timestamp);

    // =============================================================
    //                        CONSTRUCTOR
    // =============================================================

    constructor() {
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(ADMIN_ROLE, msg.sender);
    }

    // =============================================================
    //                      PUBLIC FUNCTIONS
    // =============================================================

    /**
     * @notice Choose initial path (can only be called once per address)
     * @param path The path to choose (SOVEREIGN, PRAXIS, or REFORMER)
     */
    function choosePath(UserPath path) external nonReentrant {
        require(path != UserPath.NONE, "Invalid path");
        require(users[msg.sender].currentPath == UserPath.NONE, "Path already chosen");

        users[msg.sender] = UserProfile({
            currentPath: path,
            pathChosenAt: block.timestamp,
            lastPathSwitchAt: block.timestamp,
            xpBalance: 0,
            totalDeployments: 0,
            isActive: true
        });

        pathCounts[path]++;
        totalUsers++;

        emit PathChosen(msg.sender, path, block.timestamp);
    }

    /**
     * @notice Switch to a different path (with cooldown and XP requirement)
     * @param newPath The new path to switch to
     */
    function switchPath(UserPath newPath) external nonReentrant {
        UserProfile storage user = users[msg.sender];

        require(user.currentPath != UserPath.NONE, "No path chosen yet");
        require(newPath != UserPath.NONE, "Invalid new path");
        require(newPath != user.currentPath, "Already on this path");
        require(user.isActive, "User deactivated");

        // Check cooldown
        require(
            block.timestamp >= user.lastPathSwitchAt + PATH_SWITCH_COOLDOWN,
            "Cooldown active"
        );

        // Check XP requirement (prevents constant switching)
        require(user.xpBalance >= MIN_XP_FOR_SWITCH, "Insufficient XP");

        UserPath oldPath = user.currentPath;

        // Update path counts
        pathCounts[oldPath]--;
        pathCounts[newPath]++;

        // Update user profile
        user.currentPath = newPath;
        user.lastPathSwitchAt = block.timestamp;

        emit PathSwitched(msg.sender, oldPath, newPath, block.timestamp);
    }

    // =============================================================
    //                    MODULE FUNCTIONS
    // =============================================================

    /**
     * @notice Award XP to a user (called by modules)
     * @param user Address to award XP to
     * @param amount Amount of XP to award
     * @param reason Reason for XP award (for event logging)
     */
    function awardXP(
        address user,
        uint256 amount,
        string calldata reason
    ) external onlyRole(MODULE_ROLE) {
        require(users[user].isActive, "User not active");

        users[user].xpBalance += amount;

        emit XPAwarded(user, amount, reason);
    }

    /**
     * @notice Increment deployment count for a user
     * @param user Address to increment deployment count for
     */
    function incrementDeployment(address user) external onlyRole(MODULE_ROLE) {
        require(users[user].isActive, "User not active");
        users[user].totalDeployments++;
    }

    // =============================================================
    //                      VIEW FUNCTIONS
    // =============================================================

    /**
     * @notice Get the current path of a user
     * @param user Address to query
     * @return UserPath enum value
     */
    function getUserPath(address user) external view returns (UserPath) {
        return users[user].currentPath;
    }

    /**
     * @notice Get complete user profile
     * @param user Address to query
     * @return UserProfile struct
     */
    function getUserProfile(address user) external view returns (UserProfile memory) {
        return users[user];
    }

    /**
     * @notice Check if user can switch path
     * @param user Address to check
     * @return bool True if switch is allowed
     */
    function canSwitchPath(address user) external view returns (bool) {
        UserProfile memory profile = users[user];

        if (profile.currentPath == UserPath.NONE || !profile.isActive) {
            return false;
        }

        return (block.timestamp >= profile.lastPathSwitchAt + PATH_SWITCH_COOLDOWN) &&
               (profile.xpBalance >= MIN_XP_FOR_SWITCH);
    }

    /**
     * @notice Get time remaining until path switch is available
     * @param user Address to check
     * @return uint256 Seconds remaining (0 if can switch)
     */
    function getPathSwitchCooldownRemaining(address user) external view returns (uint256) {
        UserProfile memory profile = users[user];

        if (profile.currentPath == UserPath.NONE) {
            return 0;
        }

        uint256 canSwitchAt = profile.lastPathSwitchAt + PATH_SWITCH_COOLDOWN;

        if (block.timestamp >= canSwitchAt) {
            return 0;
        }

        return canSwitchAt - block.timestamp;
    }

    /**
     * @notice Get path distribution statistics
     * @return sovereign Count of Sovereign path users
     * @return praxis Count of Praxis path users
     * @return reformer Count of Reformer path users
     */
    function getPathDistribution() external view returns (
        uint256 sovereign,
        uint256 praxis,
        uint256 reformer
    ) {
        return (
            pathCounts[UserPath.SOVEREIGN],
            pathCounts[UserPath.PRAXIS],
            pathCounts[UserPath.REFORMER]
        );
    }

    // =============================================================
    //                      ADMIN FUNCTIONS
    // =============================================================

    /**
     * @notice Deactivate a user (emergency only)
     * @param user Address to deactivate
     */
    function deactivateUser(address user) external onlyRole(ADMIN_ROLE) {
        require(users[user].isActive, "Already deactivated");
        users[user].isActive = false;
        emit UserDeactivated(user, block.timestamp);
    }

    /**
     * @notice Grant MODULE_ROLE to a contract (for modules to call awardXP)
     * @param module Address of the module contract
     */
    function grantModuleRole(address module) external onlyRole(ADMIN_ROLE) {
        _grantRole(MODULE_ROLE, module);
    }
}
