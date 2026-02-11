// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract HelloCrypto {
    string public message;

    constructor(string memory _initialMessage) {
        message = _initialMessage;
    }

    function updateMessage(string memory _newMessage) public {
        message = _newMessage;
    }
}
