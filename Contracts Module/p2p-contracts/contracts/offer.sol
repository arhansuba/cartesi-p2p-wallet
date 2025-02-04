// SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;

contract Offer {
    uint public expiryDate;
    address payable public owner;
    address payable public buyer;
    uint public value;
    string public id;
    address signer = 0x8963E134E6d22Ee9A26ac62a99964aB391ead816;

    event Withdrawal(uint amount, uint when);

    constructor(uint _value) payable {
      // seller pays ETH to the contract and requests a value in R$

        value = _value;

        expiryDate = block.timestamp + 3600;

        owner = payable(msg.sender);
    }

    function getMessageHash(
        string memory _message
    ) public pure returns (bytes32) {
        return keccak256(abi.encodePacked( _message));
    }

    function getEthSignedMessageHash(bytes32 _messageHash)
        public
        pure
        returns (bytes32)
    {
        /*
        Signature is produced by signing a keccak256 hash with the following format:
        "\x19Ethereum Signed Message\n" + len(msg) + msg
        */
        return
            keccak256(
                abi.encodePacked("\x19Ethereum Signed Message:\n32", _messageHash)
            );
    }

    function verify(
        address _signer,
        string memory _message,
        bytes memory signature
    ) public pure returns (bool) {
        bytes32 messageHash = getMessageHash(_message);
        bytes32 ethSignedMessageHash = getEthSignedMessageHash(messageHash);

        return recoverSigner(ethSignedMessageHash, signature) == _signer;
    }

    function recoverSigner(bytes32 _ethSignedMessageHash, bytes memory _signature)
        public
        pure
        returns (address)
    {
        (bytes32 r, bytes32 s, uint8 v) = splitSignature(_signature);

        return ecrecover(_ethSignedMessageHash, v, r, s);
    }

    function splitSignature(bytes memory sig)
        public
        pure
        returns (
            bytes32 r,
            bytes32 s,
            uint8 v
        )
    {
        require(sig.length == 65, "invalid signature length");

        assembly {
            /*
            First 32 bytes stores the length of the signature

            add(sig, 32) = pointer of sig + 32
            effectively, skips first 32 bytes of signature

            mload(p) loads next 32 bytes starting at the memory address p into memory
            */

            // first 32 bytes, after the length prefix
            r := mload(add(sig, 32))
            // second 32 bytes
            s := mload(add(sig, 64))
            // final byte (first byte of the next 32 bytes)
            v := byte(0, mload(add(sig, 96)))
        }

        // implicitly return (r, s, v)
    }

    function cancel() public {
        // Uncomment this line, and the import of "hardhat/console.sol", to print a log in your terminal
        //console.log("Unlock time is %o and block hash is %o", expiryDate, block.hash);

        require(block.timestamp >= expiryDate && msg.sender == owner, "You can't cancel yet");

        emit Withdrawal(address(this).balance, block.timestamp);

        owner.transfer(address(this).balance);
    }
    function claim(bytes memory signature) public {
        // Uncomment this line, and the import of "hardhat/console.sol", to print a log in your terminal
        //console.log("Unlock time is %o and block hash is %o", expiryDate, block.hash);

        require(block.timestamp < expiryDate && msg.sender == buyer, "You aren't the buyer");

        require (verify( signer, id, signature), "Invalid signature");

        emit Withdrawal(address(this).balance, block.timestamp);

        buyer.transfer(address(this).balance);
    }

    function accept() public {
      buyer = payable(msg.sender);
      id = string(abi.encodePacked(blockhash(block.number)));
    }
}