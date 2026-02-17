// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract MockGFLOToken is ERC20, Ownable {
    constructor() ERC20("GFLO Token", "GFLO") {
        _mint(msg.sender, 1_000_000_000 * 10**18);
    }
    function faucet() external {
        _mint(msg.sender, 10_000 * 10**18);
    }
}
