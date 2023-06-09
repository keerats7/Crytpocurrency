from web3 import Web3
from web3.middleware import geth_poa_middleware
from hexbytes import HexBytes
import arbitrage_config
import math

def getTXNResult(w3,tx):
    # replay the transaction locally:
    try:
        ret = w3.eth.call(tx)
        return (True,ret)
    except Exception as e: 
        return (False,str(e))
def wei_to_eth(w):
    return w/(10**18)
def tcdec_to_tc(tc, tc_decimals):
    return tc/(10**tc_decimals)

def trade():
    # Connect to blockchain
    if(arbitrage_config.config['connection_is_ipc']):
        w3 = Web3(Web3.IPCProvider(arbitrage_config.config['connection_uri']))
    else:
        w3 = Web3(Web3.WebsocketProvider('wss://andromeda.cs.virginia.edu/geth'))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    # Debug: Test connection
    # w3.is_connected()
    # ----------------------------------------------------------------------------
    # Find my current holdings (h_now = q_e * p_e + q_t * p_t)
    p_e = arbitrage_config.config['price_eth']
    p_t = arbitrage_config.config['price_tc']
    q_e = wei_to_eth(w3.eth.get_balance(arbitrage_config.config['account_address']))
    tc_address = arbitrage_config.config['tokencc_addr']
    tc_abi = arbitrage_config.itokencc_abi
    tc = w3.eth.contract(address=tc_address, abi=tc_abi)
    tc_decimals = tc.functions.decimals().call()
    q_t = tcdec_to_tc(tc.functions.balanceOf(arbitrage_config.config['account_address']).call(), tc_decimals)
    h_now = q_e * p_e + q_t * p_t
    f = arbitrage_config.config['dex_fees']
    gas_price = arbitrage_config.config['gas_price']
    # ----------------------------------------------------------------------------
    # For each DEX (only single transactions), find best eth and token trades (delta_t and delta_e)
    #                                           Calculate holdings for each of these trades
    max_profit = 0
    max_proposed_txn = ''
    params = [0.0,0.0,0.0,h_now]
    dex_abi = arbitrage_config.idex_abi
    for dex_address in arbitrage_config.config['dex_addrs']:
        dex = w3.eth.contract(address=dex_address, abi=dex_abi)
        x_d = wei_to_eth(dex.functions.x().call())
        y_d = tcdec_to_tc(dex.functions.y().call(), tc_decimals)
        k_d = dex.functions.k().call() / 10**(tc_decimals + 18)
        # Best trade in of token?
        delta_t = -1*y_d + math.sqrt((1-f) * k_d * (p_e/p_t)) # in tokens (no decimals)
        delta_t = min(q_t, delta_t) # Cannot trade more tokens than I have...
        delta_t = min(arbitrage_config.config['max_tc_to_trade'], delta_t) # Cannot trade more tc than assignment max
        delta_t = max(0, delta_t)
        # Need delta_t to be w/ decimals here, could go tokens * tc.decimals()
        proposed_txn = tc.functions.transfer(dex_address, int(delta_t * 10**tc_decimals)).build_transaction({
                'gas': 1000000,
                'gasPrice': w3.to_wei(gas_price, 'gwei'),
                'from': arbitrage_config.config['account_address'],
                'nonce': w3.eth.get_transaction_count(arbitrage_config.config['account_address']),
                'chainId': 67834503
                })
        g = 50000
        #g = w3.eth.estimate_gas(proposed_txn)
        profit = (((q_e + (1 - f)*x_d - (1 - f)*k_d/(y_d + delta_t))) * p_e + (q_t - delta_t) * p_t - wei_to_eth(g) * p_e) - h_now
        if profit > max_profit:
            params[0] = (1 - f)*x_d - (1 - f)*(k_d/(y_d + delta_t)) # +Eth
            params[1] = -1 * delta_t # -Token
            params[2] = (wei_to_eth(g) + f*x_d - f*(k_d/(y_d + delta_t))) * p_e # (w/ my understanding) (Decimals?)
            params[3] = h_now + profit
            max_profit = profit
            max_proposed_txn = proposed_txn
        # best trade in of eth?
        delta_e = -1*x_d + math.sqrt((1-f) * k_d * (p_t/p_e))
        delta_e = min(q_e, delta_e) # Cannot trade more eth than I have...
        delta_e = min(arbitrage_config.config['max_eth_to_trade'], delta_e) # Cannot trade more eth than assignment max...
        delta_e = max(0, delta_e)
        proposed_txn = {
            'nonce': w3.eth.get_transaction_count(arbitrage_config.config['account_address']),
            'to': dex_address,
            'value': w3.to_wei(delta_e * 10**18, 'wei'),
            'gas': 1000000,
            'gasPrice': w3.to_wei(gas_price, 'gwei'),
            'chainId': 67834503
        }
        #g = w3.eth.estimate_gas(proposed_txn)
        profit = (q_t + (1 - f)*y_d - (1 - f)*(k_d/(x_d + delta_e))) * p_t + (q_e - delta_e) * p_e - wei_to_eth(g) * p_e - h_now
        if profit > max_profit:
            params[0] = (-1 * delta_e)# -Eth
            params[1] = (1 - f)*y_d - (1 - f)*(k_d/(x_d + delta_e))# +Token (w/ my understanding)
            params[2] = wei_to_eth(g) * p_e + (f*y_d - f*(k_d/(x_d + delta_e))) * p_t # (w/ my understanding) (Decimals?)
            params[3] = h_now + profit
            max_profit = profit
            max_proposed_txn = proposed_txn
    # If there are profitable trades (holdings_after > holdings_before), take the best one
    if max_profit > 0:
        signed_txn = w3.eth.account.sign_transaction(max_proposed_txn, private_key=arbitrage_config.config['account_private_key'])
        ret = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    h_after = tcdec_to_tc(tc.functions.balanceOf(arbitrage_config.config['account_address']).call(), tc_decimals)*p_t +  wei_to_eth(w3.eth.get_balance(arbitrage_config.config['account_address']))*p_e   
    arbitrage_config.output(params[0], params[1], params[2], h_after)
    return 0

if __name__ == '__main__':
    trade()
