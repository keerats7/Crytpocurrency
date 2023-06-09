// SPDX-License-Identifier: MIT
// Keerat Singh (ks5hrx)

pragma solidity ^0.8.17;

import "./INFTManager.sol";
import "./ERC721.sol";

contract NFTManager is INFTManager, ERC721 {
    uint public override count;
    //A mapping that holds the tokenURI for a tokenId
    mapping (uint => string) private _tokenURI;
    constructor() ERC721("KeeratNFT","KS"){}

    function _baseURI() internal pure override returns (string memory) {
        return "https://andromeda.cs.virginia.edu/ccc/ipfs/files/";
    }
    // The tokenURI for the given tokenId;
    // Reverts for an invalid tokenId;
    // Returns the full URL
    function tokenURI(uint256 tokenId) public view virtual override(ERC721, IERC721Metadata) returns (string memory) {
        require(tokenId < count, "Token with that Id does not exist.");
        string memory baseURI = _baseURI();
        string memory targetURI = _tokenURI[tokenId];
        return string.concat(baseURI, targetURI);
    }
    // Mint a new NFT with given URI to given address;
    // Anyone can mint;
    // Duplicate URIs should cause a reversion;
    // Returns the tokenID
    function mintWithURI(address _to, string memory _uri) public override returns (uint){
        for(uint i = 0; i < count; i++){
            require((keccak256(abi.encodePacked((_uri))) != keccak256(abi.encodePacked((_tokenURI[i])))), "That URI is already taken.");
        }
        _safeMint(_to, count);
        _tokenURI[count] = _uri;
        count++;
        return count - 1;
    }
    // Mint a new NFT with given URI to the caller's account
    function mintWithURI(string memory _uri) public override returns (uint){
        return mintWithURI(msg.sender, _uri);
    }

    function supportsInterface(bytes4 interfaceId) public pure override(IERC165,ERC721) returns (bool) {
		return interfaceId == type(INFTManager).interfaceId || 
               interfaceId == type(IERC721).interfaceId ||
               interfaceId == type(IERC165).interfaceId ||
               interfaceId == type(IERC721Metadata).interfaceId;
	}


}