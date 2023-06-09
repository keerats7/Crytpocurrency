// SPDX-License-Identifier: GPL-3.0-or-later

import "./IDAO.sol";
import "./NFTManager.sol";
import "./Strings.sol";

pragma solidity ^0.8.17;

contract DAO is IDAO {
    // Public variables
    // -------------------------------------
    mapping (uint => Proposal) public override proposals;
    uint constant public override minProposalDebatePeriod = 600;
    address public override tokens;
    string constant public override purpose = "Governance token for our book club";
    mapping (address => mapping (uint => bool)) public override votedYes;
    mapping (address => mapping (uint => bool)) public override votedNo;
    uint public override numberOfProposals;
    string constant public override howToJoin = "Anyone can join!";
    uint public override reservedEther;
    address public override curator;
    // Constructor
    // ----------------------------------------------------------------
    constructor () {
        NFTManager nfts = new NFTManager();
        tokens = address(nfts);
        curator = msg.sender;
        NFTManager(tokens).mintWithURI(curator, substring(Strings.toHexString(curator),2,34)); //????
    }
    // Simple functions
    // --------------------------------------
    // Allows DAO to recieve ether
    receive() external payable {
    }
    // `msg.sender` creates a proposal to send `_amount` Wei to `_recipient`
    // with the transaction data `_transactionData`;
    // Only a member of the DAO can propose;
    // The DAO must have 'amount' ether;
    // The debating period must be greater than the minimum;
    function newProposal(address recipient, uint amount, string memory description, 
                          uint debatingPeriod) external payable returns (uint){
                              require(NFTManager(tokens).balanceOf(msg.sender) > 0, "Only members of the DAO can propose stuff");
                              require(address(this).balance - reservedEther >= amount, "DAO does not have the required funds");
                              require(debatingPeriod >= minProposalDebatePeriod, "Debating period must be at least 600 seconds");
                              proposals[numberOfProposals] = Proposal(recipient, amount, description, block.timestamp + debatingPeriod, true, false, 0, 0, msg.sender);
                              reservedEther += amount;
                              emit NewProposal(numberOfProposals, recipient, amount, description);
                              numberOfProposals++;
                              return numberOfProposals - 1;
                          }
    // Vote on proposal `_proposalID` with `_supportsProposal`;
    // Only a member of the DAO can vote;
    function vote(uint proposalID, bool supportsProposal) external {
        require(NFTManager(tokens).balanceOf(msg.sender) > 0, "Only members of the DAO can vote");
        require(proposalID < numberOfProposals, "Specified proposal does not exist");
        if(supportsProposal) {
            proposals[proposalID].yea += 1;
            votedYes[msg.sender][proposalID] = true;
        }
        else{
            proposals[proposalID].nay += 1;
            votedNo[msg.sender][proposalID] = true;
        }
        emit Voted(proposalID, supportsProposal, msg.sender);
    }
    // Closes proposal;
    // If the proposal has majority support, transfers the amount to the recipient;
    // Only a member of the DAO can close;
    // A proposal can only be closed if time is up;
    function closeProposal(uint proposalID) external {
        require(NFTManager(tokens).balanceOf(msg.sender) > 0, "Only members of the DAO can close");
        require(proposalID < numberOfProposals, "Specified proposal does not exist");
        require(proposals[proposalID].votingDeadline <= block.timestamp, "The deadline is not over.");
        if(proposals[proposalID].yea > proposals[proposalID].nay){
            (bool success, ) = payable(proposals[proposalID].recipient).call{value: proposals[proposalID].amount}(""); // Proposal passed, transfer amount to recip
            require(success, "Failed to transfer ETH");
            proposals[proposalID].proposalPassed = true;
        }
        proposals[proposalID].open = false;
        reservedEther -= proposals[proposalID].amount;
        emit ProposalClosed(proposalID, proposals[proposalID].proposalPassed);
    }
    // Is this address a member of the DAO?
    function isMember(address who) external view returns (bool) {
        return NFTManager(tokens).balanceOf(who) > 0;
    }
    // Adds this address as a member;
    // Only current members can add other members;
    // Members cannot be added twice;
    function addMember(address who) external {
        require(NFTManager(tokens).balanceOf(msg.sender) > 0, "Only members of the DAO can close");
        require(NFTManager(tokens).balanceOf(who) == 0, "This address is already a member");
        NFTManager(tokens).mintWithURI(who, substring(Strings.toHexString(who),2,34));
    }
    // Anybody can become a member;
    // Rerverts if members request again;
    function requestMembership() external {
        require(NFTManager(tokens).balanceOf(msg.sender) == 0, "This address is already a member");
        NFTManager(tokens).mintWithURI(msg.sender, substring(Strings.toHexString(msg.sender),2,34));
    }
    // Provided function to URIs;
    function substring(string memory str, uint startIndex, uint endIndex) public pure returns (string memory) {
        bytes memory strBytes = bytes(str);
        bytes memory result = new bytes(endIndex-startIndex);
        for(uint i = startIndex; i < endIndex; i++)
            result[i-startIndex] = strBytes[i];
        return string(result);
    }

    function supportsInterface(bytes4 interfaceId) external override pure returns (bool) {
		return interfaceId == type(IDAO).interfaceId || 
               interfaceId == type(IERC165).interfaceId;
	}

}

