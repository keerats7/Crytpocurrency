// SPDX-License-Identifier: GPL-3.0-or-later

pragma solidity ^0.8.17;

// x is the ether liquidity, with 18 decimals
// y is the token liquidity, with a variable number of decimals
// k = x * y, and will have somewhere around 30 decimals
import "./IDEX.sol";
import "./IEtherPriceOracle.sol";
import "./ERC20.sol";

contract DEX is IDEX {
    // Internal variables
    // ----------------------------------------------------------------
    bool internal poolCreated;
    address internal deployer;
    bool internal adjustingLiquidity;
    // Public variables
    // ----------------------------------------------------------------
    uint public i;
    // k = x * y
    uint public override k;
    // ETH (in 10^18)
    uint public override x;
    // TCC in (10^10)
    uint public override y;
    // Amount of ETH an address has in the pool
    mapping (address => uint) public override etherLiquidityForAddress;
    // Amount of TCC an address has in the pool
    mapping (address => uint) public override tokenLiquidityForAddress;
    // The numerator of the fee fraction
    uint public override feeNumerator;
    // The denominator of the fee fraction
    uint public override feeDenominator;
    // Amount of fees accumulated, in wei, for all addresses so far
    uint public override feesEther;
    // Amount of fees accumulated, in TCC, for all addresses so far
    uint public override feesToken;
    // Address of the etherPricer contract
    address public override etherPricer;
    // Address of the ERC-20 token manager contract
    address public override erc20Address;
    // Constructor
    // ----------------------------------------------------------------
    constructor () {
        poolCreated = false;
        deployer = msg.sender;
        adjustingLiquidity = false;
    }
    // Simple functions
    // ----------------------------------------------------------------
    // The number of decimals of the token
    function decimals() external override view returns (uint) {
        return ERC20(erc20Address).decimals();
    }
    // The symbol of the token
    function symbol() external override view returns (string memory) {
        return ERC20(erc20Address).symbol();
    }
    // The price of 1 ETH (in cents);
    // Constant: 0x929765249087e80A32e32137888D7e988d4ECad2
    // Variable: 0x2bEB4D4d7eA1eA9024a5C1e6e2E375B5CFd2C288
    function getEtherPrice() external override view returns (uint) {
        return IEtherPriceOracle(etherPricer).price();
    }
    // The price of 1 TCC (in cents);
    // Assumes the ETH and TCC in the pool are equal in value
    function getTokenPrice() external override view returns (uint) {
        uint ethPrice = IEtherPriceOracle(etherPricer).price();
        return ethPrice * (x * (10**(ERC20(erc20Address).decimals()))) / (y * (10**18));
    }
    // The liquidity of the pool (in cents)
    function getPoolLiquidityInUSDCents() external override view returns (uint) {
        uint ethPrice = IEtherPriceOracle(etherPricer).price();
        return 2 * x * ethPrice / (10**18);
    }
    // (Re)sets the ether pricer contract
    function setEtherPricer(address p) external {
        etherPricer = p;
    }
    // A tuple of the DEX info in the order: 
    // 0: the address of *this* DEX contract (address)
    // 1: token cryptocurrency abbreviation (string memory)
    // 2: token cryptocurrency name (string memory)
    // 3: ERC-20 token cryptocurrency address (address)
    // 4: k (uint)
    // 5: ether liquidity (uint)
    // 6: token liquidity (uint)
    // 7: fee numerator (uint)
    // 8: fee denominator (uint)
    // 9: token decimals (uint)
    // 10: fees collected in ether (uint)
    // 11: fees collected in the token CC (uint)
    function getDEXinfo() external view returns (address, string memory, string memory, 
                            address, uint, uint, uint, uint, uint, uint, uint, uint) {
                                return (address(this), ERC20(erc20Address).symbol(), ERC20(erc20Address).name(), 
                                        erc20Address, k, x, y, feeNumerator, feeDenominator, ERC20(erc20Address).decimals(),
                                        feesEther, feesToken);
                            }
    // To be used later...
    function reset() external pure {
        revert();
    }
    // This contract supports IDEX, IERC165, and IERC20Receiver
    function supportsInterface(bytes4 interfaceId) external override pure returns (bool) {
		return interfaceId == type(IDEX).interfaceId || 
               interfaceId == type(IERC165).interfaceId ||
               interfaceId == type(IERC20Receiver).interfaceId;
	}
    // Not-as-simple functions
    // ----------------------------------------------------------------
    // Creates a liquidity pool with a certain amount of ETH and TCC;
    // The fee percentage is defined;
    // The related token and etherPricer contracts are given;
    // Requires the DEX contract has been approved for given TCC by sender;
    // Can only be called once;
    // Only the deployer of the contract can call this
    function createPool(uint _tokenAmount, uint _feeNumerator, uint _feeDenominator, 
                        address _erc20token, address _etherPricer) external payable {
                            require(!poolCreated, "A liquidity pool has already been created.");
                            require(msg.sender == deployer, "Only the deployer of the contract can create a pool.");
                            require(ERC20(_erc20token).allowance(msg.sender, address(this)) >= _tokenAmount, "This contract needs to first be approved for the specified token amount.");
                            adjustingLiquidity = true;
                            ERC20(_erc20token).transferFrom(msg.sender, address(this), _tokenAmount);
                            adjustingLiquidity = false;
                            x = msg.value;
                            y = _tokenAmount;
                            k = x * y;
                            feeNumerator = _feeNumerator;
                            feeDenominator = _feeDenominator;
                            etherLiquidityForAddress[msg.sender] = x;
                            tokenLiquidityForAddress[msg.sender] = y;
                            erc20Address = _erc20token;
                            etherPricer = _etherPricer;
                            poolCreated = true;
                        }
    // Adds liquidity to the pool;
    // ETH is sent with the function call, TCC is calculated to maintain current exchange ratio;
    // Requires the DEX contract has been approved for given TCC by sender
    function addLiquidity() external payable {
        uint ethAmount = msg.value;
        uint tokenAmount = (ethAmount * y) / x;
        adjustingLiquidity = true;
        ERC20(erc20Address).transferFrom(msg.sender, address(this), tokenAmount);
        adjustingLiquidity = false;
        x += ethAmount;
        y += tokenAmount;
        k = x * y;
        etherLiquidityForAddress[msg.sender] += ethAmount;
        tokenLiquidityForAddress[msg.sender] += tokenAmount;
        emit liquidityChangeEvent();
    }
    // Transfers the sender back their liquidity;
    // Requires that they own that much liquidity
    // How do liquidity mappings update? Sum of mappings should ewual x and y;
    // If people swap tokens for ether, then someone removes their liquidity,
    // That could be higher than the balance of the DEX if we don't take out liquidity for people.
    function removeLiquidity(uint amountEther) external {
        require(etherLiquidityForAddress[msg.sender] >= amountEther, "Sender does not have this much ETH in the pool.");
        uint amountToken = amountEther * y / x;
        (bool success, ) = payable(msg.sender).call{value: amountEther}("");
        require (success, "payment didn't work");
        adjustingLiquidity = true;
        ERC20(erc20Address).transfer(msg.sender, amountToken);
        adjustingLiquidity = false;
        etherLiquidityForAddress[msg.sender] -= amountEther;
        tokenLiquidityForAddress[msg.sender] -= amountToken;
        x -= amountEther;
        y -= amountToken;
        k = x * y;
        emit liquidityChangeEvent();
    }
    // Swaps ether for token;
    // What if pool doesn't have that much token?
    receive() external payable {
        uint ethAmount = msg.value;
        uint tokenAmount = y - k/(x + ethAmount);
        uint fee = tokenAmount * feeNumerator/feeDenominator;
        ERC20(erc20Address).transfer(msg.sender, tokenAmount - fee);
        x += ethAmount;
        y -= tokenAmount;
        // etherLiquidityForAddress[msg.sender] += ethAmount;
        // tokenLiquidityForAddress[msg.sender] -= tokenAmount;
        feesToken += fee;
        emit liquidityChangeEvent();
    }
    // Swaps token for ether;
    // Rn, if I call transfer, it doesn't look like it's going into this function
    // Return I'm not too sure about...
    function onERC20Received(address from, uint amount, address erc20) external override returns (bool) {
        i+=1;
        if(adjustingLiquidity) {return true;}
        require(erc20==erc20Address, "This DEX does not support those tokens."); // Changed this line
        uint ethAmount = x - k/(y + amount);
        uint fee = ethAmount * feeNumerator/feeDenominator;
        (bool success, ) = payable(from).call{value: ethAmount - fee}("");
        require (success, "payment didn't work");
        x -= ethAmount;
        y += amount;
        // etherLiquidityForAddress[from] -= ethAmount;
        // tokenLiquidityForAddress[from] += amount;
        feesEther += fee;
        emit liquidityChangeEvent();
        return true;
    }



    


}