// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

contract SimpleNumber {

    uint storedNumber;

    function getStoredNumber() view public returns(uint) {
        return  storedNumber;
    }

    function updateStoredNumber(uint newValue) public returns(uint) {
        storedNumber = newValue;

        return storedNumber;
    }

}
