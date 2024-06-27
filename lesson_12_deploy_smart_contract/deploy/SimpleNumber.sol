// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

contract SimpleNumber {

    uint number;

    function getNumber() view public returns(uint) {
        return  number;
    }

    function setNumber(uint newValue) public returns(uint) {
        number = newValue;

        return number;
    }

}
