// SPDX-License-Identifier: GPL-3.0-or-later
// Keerat Singh (ks5hrx)

pragma solidity ^0.8.17;

import "./ITokenCC.sol";
import "./ERC20.sol";
import "./IERC20Receiver.sol";

contract TokenCC is ITokenCC, ERC20 {
    uint public i;
    constructor() ERC20("LoveLetters", "LOVE") {
        _mint(msg.sender, 1000000 * 10**10);
    }
    //reverts
    function requestFunds() public pure override {
        revert();
    }
    //How precise is the decimal?
    function decimals() public pure override(ERC20, IERC20Metadata) returns (uint8) {
        return 10;
    }

    // Whenever TokenCC is transferred to another contract,
    // it will notify that contract that it recieved ERC20 tokens.
    function _afterTokenTransfer(address from, address to, uint256 amount) internal override {
        if ( to.code.length > 0  && from != address(0) && to != address(0) ) {
            // token recipient is a contract, notify them
            i+=1;
            try IERC20Receiver(to).onERC20Received(from, amount, address(this)) returns (bool success) {
                require(success,"ERC-20 receipt rejected by destination of transfer");
            } catch {
                // the notification failed (maybe they don't implement the `IERC20Receiver` interface?)
                // we choose to ignore this case
            }
        }
    }

    function supportsInterface(bytes4 interfaceId) external override pure returns (bool) {
		return interfaceId == type(ITokenCC).interfaceId || 
               interfaceId == type(IERC20).interfaceId ||
               interfaceId == type(IERC165).interfaceId ||
               interfaceId == type(IERC20Metadata).interfaceId;
	}
}