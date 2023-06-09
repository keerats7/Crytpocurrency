import hexbytes

# The configuration options to connect to the blockchain and the DEXes
config = {
    'account_address': '0x17d56256bbB6558970A31fb79Ba6b02B73F2C8D5',
    'account_private_key': hexbytes.HexBytes('bf7e01c856af39bcd6aa9b35f107c3343798888fda809a45f3fac18350ff8b22'),
    'connection_is_ipc': False,
    'connection_uri': '/Users/keeratsingh/Documents/Crypto/S4/ethprivate',
    'price_eth': 100.00,
    'price_tc': 10.0,
    'dex_addrs': [
              #'0xcb81D0fa99e94908533b772EC44623315f8E7120', # d4 dex
              #'0x48bb9E41909AF457e1199B357B1648153764025b', # d6 dex
              #'0xfBf9992Db8d694B35200F91A63d68885f13FbBF9', # d8 dex
              '0xc7EF3F007F499252B9b4166573313DAfDA28034a', # d10 dex
              '0x5DeF5118a07856f9a7F8EEd956777470574c601B', # d12 dex
              '0x0867445b7DF22aB4F5767474544D7e8e10D301f4', # d20 dex
             ],
    'tokencc_addr': '0x76ffa06b06217d56a5F25Ef8B9f9EfA7c8120905',
    'max_eth_to_trade': 10.0,
    'max_tc_to_trade': 100.0,
    'gas_price': 1, # in gwei
    'dex_fees': 0.005, # that's 1/2 of a percernt
}

# This will print the output into the format required by the homework.  It
# should not be changed.
def output(ethAmt, tcAmt, fees, holdings):
    if ethAmt == 0 and tcAmt == 0:
        print("No profitable arbitrage trades available")
        return
    assert ethAmt * tcAmt < 0, "Exactly one of ethAmt and tcAmt should be negative, the other positive"
    if ethAmt < 0:
        print("Exchanged %.4f ETH for %.4f TC; fees: %.2f USD; prices: ETH %.2f USD, TC: %.2f USD; holdings: %.2f USD" %
              (ethAmt, tcAmt, fees, config['price_eth'], config['price_tc'], holdings))
    else:
        print("Exchanged %.4f TC for %.4f ETH; fees: %.2f USD; prices: ETH %.2f USD, TC: %.2f USD; holdings: %.2f USD" %
              (tcAmt, ethAmt, fees, config['price_eth'], config['price_tc'], holdings))

# This is the ABI for IDEX.sol (this includes the functions inherited from IERC165 and IERC20Receiver)
idex_abi = '[{"anonymous":false,"inputs":[],"name":"liquidityChangeEvent","type":"event"},{"inputs":[],"name":"addLiquidity","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_tokenAmount","type":"uint256"},{"internalType":"uint256","name":"_feeNumerator","type":"uint256"},{"internalType":"uint256","name":"_feeDenominator","type":"uint256"},{"internalType":"address","name":"_erc20token","type":"address"},{"internalType":"address","name":"_etherPricer","type":"address"}],"name":"createPool","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"erc20Address","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"who","type":"address"}],"name":"etherLiquidityForAddress","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"etherPricer","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"feeDenominator","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"feeNumerator","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"feesEther","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"feesToken","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getDEXinfo","outputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"string","name":"","type":"string"},{"internalType":"string","name":"","type":"string"},{"internalType":"address","name":"","type":"address"},{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getEtherPrice","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getPoolLiquidityInUSDCents","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getTokenPrice","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"k","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"address","name":"erc20","type":"address"}],"name":"onERC20Received","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountEther","type":"uint256"}],"name":"removeLiquidity","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"p","type":"address"}],"name":"setEtherPricer","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"who","type":"address"}],"name":"tokenLiquidityForAddress","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"x","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"y","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"stateMutability":"payable","type":"receive"}]';

# This is the ABI for ITokenCC.sol (this includes the functions inherited from IERC20Metadata, IERC20, and IERC165)
itokencc_abi = '[{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"requestFunds","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"}]';

# This function will attempt to determine a return value or why a transaction
# reverted.  It will return one of three values:
# - None when it encounters an error (not when it encounters a revert)
# - (True,<ret>) if the TXN returned a value; the value is <ret>
# - (False,<str>) if the TXN reverted; the revert reason is <str>
def getTXNResult(w3,txhash):
    try:
        tx = w3.eth.get_transaction(txhash)
    except Exception as e:
        print("Error getting transaction:",e)
        return None
    replay_tx = {
        'to': tx['to'],
        'from': tx['from'],
        'value': tx['value'],
        'data': tx['input'],
        'gas': tx['gas'],
    }
    # replay the transaction locally:
    try:
        ret = w3.eth.call(replay_tx, tx.blockNumber - 1)
        return (True,ret)
    except Exception as e: 
        return (False,str(e))
