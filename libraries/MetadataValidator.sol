// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

library MetadataValidator {
    function isValidSovWeb(string memory sovWeb) internal pure returns (bool) {
        bytes memory b = bytes(sovWeb);
        if (b.length < 3 || b.length > 64) return false;
        for (uint256 i = 0; i < b.length; i++) {
            bytes1 char = b[i];
            if (!(char >= 0x61 && char <= 0x7A) && !(char >= 0x30 && char <= 0x39) && !(char == 0x2E)) return false;
        }
        return true;
    }
    function hashMetadata(string memory metadataUri) internal pure returns (bytes32) {
        require(bytes(metadataUri).length > 0, "Empty");
        return keccak256(abi.encodePacked(metadataUri));
    }
    function isValidSymbol(string memory symbol) internal pure returns (bool) {
        bytes memory b = bytes(symbol);
        if (b.length < 3 || b.length > 8) return false;
        for (uint256 i = 0; i < b.length; i++) {
            bytes1 char = b[i];
            if (!(char >= 0x41 && char <= 0x5A) && !(char >= 0x30 && char <= 0x39)) return false;
        }
        return true;
    }
}
