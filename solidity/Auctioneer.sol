// SPDX-License-Identifier: GPL-3.0-or-later

pragma solidity ^0.8.17;

import "./IAuctioneer.sol";
import "./NFTManager.sol";

contract Auctioneer is IAuctioneer {
    uint public override num_auctions;
    address public override nftmanager;
    uint public override totalFees; // In wei
    uint public override uncollectedFees; // In wei
    mapping (uint => Auction) public override auctions;
    address public override deployer;
    constructor() {
        NFTManager nfts = new NFTManager();
        nftmanager = address(nfts);
        deployer = msg.sender;
    }
    // Pays uncollectedFees to deployer;
    // Can only be called by the deployer
    function collectFees() external override {
        require(msg.sender == deployer, "Only the deployer of this auction can call this function.");
        require(uncollectedFees > 0, "No fees to collect.");
        (bool success, ) = payable(deployer).call{value: uncollectedFees}("");
        require(success, "Failed to transfer ETH");
        totalFees += uncollectedFees;
        uncollectedFees = 0;
    }

    // The auctioneer will transfer ownership of sender’s NFT to itself, and revert if it cannot do so;
    // An Auction struct will be created, starting the auction;
    // Multiple auctions cannot be held on one NFT;
    // Auctions must be held for a non-zero duration;
    // data cannot be an empty string;
    // Only the owner of a NFT can start an auction for it
    function startAuction(uint m, uint h, uint d, string memory data, uint reserve, uint nftid) external override returns (uint) {
        require(msg.sender == NFTManager(nftmanager).ownerOf(nftid), "Only the owner of that NFT can start an auction for it.");
        require(bytes(data).length != 0, "Data cannot be empty.");
        require(m > 0 || h > 0 || d > 0, "Auction duration must be non-zero.");
        for(uint i = 0; i < num_auctions; i++){
            if(auctions[i].active){
                require(auctions[i].nftid != nftid, "Multiple active auctions cannot be held on one NFT.");
            }
        }
        NFTManager(nftmanager).transferFrom(msg.sender, address(this), nftid);
        uint endTime = block.timestamp + 
                        m * 1 minutes + h * 1 hours + d * 1 days;
        auctions[num_auctions] = Auction(num_auctions, 0, data, reserve, address(0), msg.sender, nftid, endTime, true);
        emit auctionStartEvent(num_auctions);
        num_auctions += 1;
        return num_auctions - 1;
    }

    // This closes the given auction;
    // If bidded on, the highest bid is transferred from the contract to the initiator,
    // And the NFT is transferred to the bidder;
    // The contract will keep 1% of fees;
    // If not bidded on, the NFT is transferred back to the initiator;
    // Requires auction's time to have expired
    function closeAuction(uint id) external override {
        require(id < num_auctions, "Auction with specified id does not exist.");
        require(auctions[id].active, "Specified auction is inactive.");
        require(block.timestamp >= auctions[id].endTime, "This auction has not passed its end time.");
        if(auctions[id].num_bids > 0){
            uncollectedFees += auctions[id].highestBid / 100;
            uint valueToInitiator = 99 * auctions[id].highestBid / 100; // Contract keeps 1% of highest bid
            (bool success, ) = payable(auctions[id].initiator).call{value: valueToInitiator}(""); // Transfer winnings to auction's initiator
            require(success, "Failed to transfer ETH");
            NFTManager(nftmanager).transferFrom(address(this), auctions[id].winner, auctions[id].nftid);
            emit auctionCloseEvent(id);
        }
        else{
            NFTManager(nftmanager).transferFrom(address(this), auctions[id].initiator, auctions[id].nftid);
        }
        auctions[id].active = false;
    }
    // Places bid on the specified auction;
    // The auction must be valid, active, and not over;
    // The bid must be greater than the previous highest bid;
    // The bid will be transferred
    function placeBid(uint id) payable external {
        require(id < num_auctions, "Auction with specified id does not exist.");
        require(auctions[id].active, "Specified auction is inactive.");
        require(block.timestamp < auctions[id].endTime, "This auction has ended.");
        require(msg.value > auctions[id].highestBid, "Bid must be greater than the highest bid.");
        // Sender transfers bid to contract (payable function);
        // reverts if they don't have enough money
        // This is a valid bid, refund the previous highest bidder (if not the first bid)
        if(auctions[id].num_bids > 0){
            (bool success, ) = payable(auctions[id].winner).call{value: auctions[id].highestBid}(""); // Transfer previous bid back
            require(success, "Failed to transfer ETH");
        }
        // Update Auction struct to reflect new winner
        auctions[id].winner = msg.sender;
        auctions[id].highestBid = msg.value;
        auctions[id].num_bids += 1;
        emit higherBidEvent(id);
    }

    // Returns the time left (in seconds) for a given auction;
    // The auction must be valid and active;
    function auctionTimeLeft(uint id) external view returns (uint) {
        require(id < num_auctions, "Auction with specified id does not exist.");
        require(auctions[id].active, "Specified auction is inactive.");
        if (block.timestamp < auctions[id].endTime) {
            return auctions[id].endTime - block.timestamp;
        }
        else{
            return 0;
        }
    }

    function supportsInterface(bytes4 interfaceId) external override pure returns (bool) {
		return interfaceId == type(IAuctioneer).interfaceId || 
               interfaceId == type(IERC165).interfaceId;
	}
}