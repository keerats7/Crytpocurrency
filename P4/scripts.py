#!/usr/bin/python3

# This is the homework submission file for the BTC Scripting homework, which
# can be found at http://aaronbloomfield.github.io/ccc/hws/btcscript.  That
# page describes how to fill in this program.


from bitcoin.wallet import CBitcoinAddress, CBitcoinSecret, P2PKHBitcoinAddress
from bitcoin import SelectParams
from bitcoin.core import CMutableTransaction
from bitcoin.core.script import *
from bitcoin.core import x


#------------------------------------------------------------
# Do not touch: change nothing in this section!

# ensure we are using the bitcoin testnet and not the real bitcoin network
SelectParams('testnet')

# The address that we will pay our tBTC to -- do not change this!
tbtc_return_address = CBitcoinAddress('mv4rnyY3Su5gjcDNzbMLKBQkBicCtHUtFB') # https://coinfaucet.eu/en/btc-testnet/

# The address that we will pay our BCY to -- do not change this!
bcy_dest_address = CBitcoinAddress('mgBT4ViPjTTcbnLn9SFKBRfGtBGsmaqsZz')

# Yes, we want to broadcast transactions
broadcast_transactions = True

# Ensure we don't call this directly
if __name__ == '__main__':
    print("This script is not meant to be called directly -- call bitcoinctl.py instead")
    exit()


#------------------------------------------------------------
# Setup: your information

# Your UVA userid
userid = 'ks5hrx'

# Enter the BTC private key and invoice address from the setup 'Testnet Setup'
# section of the assignment.  
my_private_key_str = "cUbXPwVFdrmt6Qd5whnRE6iwTw7bpq2s5gBxpHHjdcz7YVTvHx4E"
my_invoice_address_str = "n3vREdkERugxjYcrHYvmUWhkf7hFLeXNym"

# Enter the transaction ids (TXID) from the funding part of the 'Testnet
# Setup' section of the assignment.  Each of these was provided from a faucet
# call.  And obviously replace the empty string in the list with the first
# one you obtain..
txid_funding_list = ["a43c71ad3c61ab8e06b4421bfe8d287faf1f19e48bd76d4f64756827ff7d1e68"]

# These conversions are so that you can use them more easily in the functions
# below -- don't change these two lines.
if my_private_key_str != "":
    my_private_key = CBitcoinSecret(my_private_key_str)
    my_public_key = my_private_key.pub


#------------------------------------------------------------
# Utility function(s)

# This function will create a signature of a given transaction.  The
# transaction itself is passed in via the first three parameters, and the key
# to sign it with is the last parameter.  The parameters are:
# - txin: the transaction input of the transaction being signed; type: CMutableTxIn
# - txout: the transaction output of the transaction being signed; type: CMutableTxOut
# - txin_scriptPubKey: the pubKey script of the transaction being signed; type: list
# - private_key: the private key to sign the transaction; type: CBitcoinSecret
def create_CHECKSIG_signature(txin, txout, txin_scriptPubKey, private_key):
    tx = CMutableTransaction([txin], [txout])
    sighash = SignatureHash(CScript(txin_scriptPubKey), tx, 0, SIGHASH_ALL)
    return private_key.sign(sighash) + bytes([SIGHASH_ALL])


#------------------------------------------------------------
# Testnet Setup: splitting coins

# The transaction ID that is to be split -- the assumption is that it is the
# transaction hash, above, that funded your account with tBTC.  You may have
# to split multiple UTXOs, so if you are splitting a different faucet
# transaction, then change this appropriately. It must have been paid to the
# address that corresponds to the private key above
txid_split = txid_funding_list[0]

# After all the splits, you should have around 10 (or more) UTXOs, all for the
# amount specified in this variable. That amount should not be less than
# 0.0001 BTC, and can be greater.  It will make your life easier if each
# amount is a negative power of 10, but that's not required.
split_amount_to_split = 0.0009 #0.01434476 from https://live.blockcypher.com/btc-testnet/address/n3vREdkERugxjYcrHYvmUWhkf7hFLeXNym/
# 0.001 BCY from https://live.blockcypher.com/bcy/address/C93tWJoQXTkVMooaNmWL3poWPa16BaVk4N/
# How much BTC is in that UTXO; look this up on https://live.blockcypher.com
# to get the correct amount.
split_amount_after_split = 0.00001 #0.001 for first split

# How many UTXO indices to split it into -- you should not have to change
# this!  Note that it will actually split into one less, and use the last one
# as the transaction fee.
split_into_n = int(split_amount_to_split/split_amount_after_split)
# Ran in shell: ./bitcoinctl.py split 1
# The transaction IDs obtained after successfully splitting the tBTC.
txid_split_list = ["76d9d73b33807bbcafe482ca2babbb752da060d5849246c85ab10fc4f796b723"]


#------------------------------------------------------------
# Global settings: some of these will need to be changed for EACH RUN

# The transaction ID that is being redeemed for the various parts herein --
# this should be the result of the split transaction, above; thus, the
# default is probably sufficient.
txid_utxo = txid_split_list[0]

# This is likely not needed.  The bitcoinctl.py will take a second
# command-line parmaeter, which will override this value.  You should use the
# second command-line parameter rather than this variable. The index of the
# UTXO that is being spent -- note that these indices are indexed from 0.
# Note that you will have to change this for EACH run, as once a UTXO index
# is spent, it can't be spent again.  If there is only one index, then this
# should be set to 0.
utxo_index = -1

# How much tBTC to send -- this should be LESS THAN the amount in that
# particular UTXO index -- if it's not less than the amount in the UTXO, then
# there is no miner fee, and it will not be mined into a block.  Setting it
# to 90% of the value of the UTXO index is reasonable.  Note that the amount
# in a UTXO index is split_amount_to_split / split_into_n.
send_amount = split_amount_after_split * 0.9


#------------------------------------------------------------
# Part 1: P2PKH transaction

# This defines the pubkey script (aka output script) for the transaction you
# are creating.  This should be a standard P2PKH script.  The parameter is:
# - address: the address this transaction is being paid to; type:
#   P2PKHBitcoinAddress
def P2PKH_scriptPubKey(address):
    return [ 
             OP_DUP, OP_HASH160, address, OP_EQUALVERIFY, OP_CHECKSIG
           ]

# This function provides the sigscript (aka input script) for the transaction
# that is being redeemed.  This is for a standard P2PKH script.  The
# parameters are:
# - txin: the transaction input of the UTXO being redeemed; type:
#   CMutableTxIn
# - txout: the transaction output of the UTXO being redeemed; type:
#   CMutableTxOut
# - txin_scriptPubKey: the pubKey script (aka output script) of the UTXO being
#   redeemed; type: list
# - private_key: the private key of the redeemer of the UTXO; type:
#   CBitcoinSecret
def P2PKH_scriptSig(txin, txout, txin_scriptPubKey, private_key):
    tx = CMutableTransaction([txin], [txout])
    sighash = SignatureHash(CScript(txin_scriptPubKey), tx, 0, SIGHASH_ALL)
    sig = private_key.sign(sighash) + bytes([SIGHASH_ALL])
    public_key = private_key.pub #type CPubKey
    #address = P2PKHBitcoinAddress.from_pubkey(public_key) #BTC address is a hashed public key
    return [ 
             sig, public_key
           ]

# The transaction hash received after the successful execution of this part
txid_p2pkh = "a7dbe37d58632094e1020a28ba9a210c8d6d55d4b73ca65a505e188d2b37dbff"


#------------------------------------------------------------
# Part 2: puzzle transaction

# These two values are constants that you should choose -- they should be four
# digits long.  They need to allow for only integer solutions to the linear
# equations specified in the assignment.
puzzle_txn_p = 5001
puzzle_txn_q = 5002

# These are the solutions to the linear equations specified in the homework
# assignment.  You can use an online linear equation solver to find the
# solutions.
puzzle_txn_x = 5000
puzzle_txn_y = 1

# This function provides the pubKey script (aka output script) that requres a
# solution to the above equations to redeem this UTXO.
def puzzle_scriptPubKey():
    return [ 
             OP_2DUP, OP_ADD, puzzle_txn_p, OP_EQUALVERIFY, OP_DUP, OP_ADD, OP_ADD, puzzle_txn_q, OP_EQUAL
           ]

# This function provides the sigscript (aka input script) for the transaction
# that you are redeeming.  It should only provide the two values x and y, but
# in the order of your choice.
def puzzle_scriptSig():
    return [ 
             puzzle_txn_x, puzzle_txn_y
           ]

# The transaction hash received after successfully submitting the first
# transaction above (part 2a)
txid_puzzle_txn1 = "c1d17f124cd9a1744838d68542fe52bee9c52fa8b7eabc2a9b819e4a932469be"

# The transaction hash received after successfully submitting the second
# transaction above (part 2b)
txid_puzzle_txn2 = "42b496e66e66524bf0b1bdcf718b2affbf0c69e95f39734addc8a0109911bcfb"


#------------------------------------------------------------
# Part 3: Multi-signature transaction

# These are the public and private keys that need to be created for alice,
# bob, and charlie
alice_private_key_str = "cSzfSHtrzkuN4Y8xnDcfqqQDYSta6V2ix577cYG3VVN95xoN71iN"
alice_invoice_address_str = "msKbYYxFwJvZ29dCxmVAYByYt6toBLwHrb"
bob_private_key_str = "cVakCRjoDkX53RUEMCv6hW8d2mZtce7uMi12td8aYDtwEWBFjCQN"
bob_invoice_address_str = "mzkxkJ74mbJwHbSQ95oQMfVeKYa5bSMQPf"
charlie_private_key_str = "cSmHXJBjuxpG9AwEYWf5EkfxiwjwtcNPotKsHF3mawp6VuCGxosJ"
charlie_invoice_address_str = "mfwChiwryhm4zLQyFxZHYJUc1FrpEywDEv"

# These three lines convert the above strings into the type that is usable in
# a script -- you should NOT modify these lines.
if alice_private_key_str != "":
    alice_private_key = CBitcoinSecret(alice_private_key_str)
if bob_private_key_str != "":
    bob_private_key = CBitcoinSecret(bob_private_key_str)
if charlie_private_key_str != "":
    charlie_private_key = CBitcoinSecret(charlie_private_key_str)

# This function provides the pubKey script (aka output script) that will
# require multiple different keys to allow redeeming this UTXO.  It MUST use
# the OP_CHECKMULTISIGVERIFY opcode.  While there are no parameters to the
# function, you should use the keys above for alice, bob, and charlie, as
# well as your own key.
def multisig_scriptPubKey():
    alice_pubkey = alice_private_key.pub
    bob_pubkey = bob_private_key.pub
    charlie_pubkey = charlie_private_key.pub
    #PubKey script pushes the pub key hashes, assuming those are address(privkey.pub)
    return [ 
            OP_2, alice_pubkey, bob_pubkey, charlie_pubkey, OP_3, OP_CHECKMULTISIGVERIFY, my_public_key, OP_CHECKSIG
           ]

# This function provides the sigScript (aka input script) that can redeem the
# above transaction.  The parameters are the same as for P2PKH_scriptSig
# (), above.  You also will need to use the keys for alice, bob, and charlie,
# as well as your own key.  The private key parameter used is the global
# my_private_key.
def multisig_scriptSig(txin, txout, txin_scriptPubKey):
    bank_sig = create_CHECKSIG_signature(txin, txout, txin_scriptPubKey, my_private_key)
    alice_sig = create_CHECKSIG_signature(txin, txout, txin_scriptPubKey, alice_private_key)
    bob_sig = create_CHECKSIG_signature(txin, txout, txin_scriptPubKey, bob_private_key)
    charlie_sig = create_CHECKSIG_signature(txin, txout, txin_scriptPubKey, charlie_private_key)
    return [ 
             bank_sig, OP_0, alice_sig, bob_sig
           ]

# The transaction hash received after successfully submitting the first
# transaction above (part 3a)
txid_multisig_txn1 = "fe3ce3d3253eff687c1776efc6732f77e632bd379e9a17ec7b1e1b062b26d744"

# The transaction hash received after successfully submitting the second
# transaction above (part 3b)
txid_multisig_txn2 = "5f5e924a3322b660287688349c3bfa0dbf3dd234f37be6bdeb2b4daa3f18b9fb"


#------------------------------------------------------------
# Part 4: cross-chain transaction

# This is the API token obtained after creating an account on
# https://accounts.blockcypher.com/.  This is optional!  But you may want to
# keep it here so that everything is all in once place.
blockcypher_api_token = "7d7c8fb9386047feaf73d0464b636c36"

# These are the private keys and invoice addresses obtained on the BCY test
# network.
my_private_key_bcy_str = "97198a0de3f7ba307283fc54b7ab9f8580aa55137498ee21a97da8217bdd2bd5"
my_invoice_address_bcy_str = "CEfhjWLJqj1ZCFT3PkAcCDueLuMCgK61TL"
bob_private_key_bcy_str = "e8523f10b63014d2c6c29a2eb3b38561f7c4423a1123fafd893a25c09283c5ab"
bob_invoice_address_bcy_str = "C93tWJoQXTkVMooaNmWL3poWPa16BaVk4N"

# This is the transaction hash for the funding transaction for Bob's BCY
# network wallet.
txid_bob_bcy_funding = "3b7a5cd2fdfc7e190e118b06f1e5fbdf7bae0d3af2d4ce2a199f07fede6518e1"

# This is the transaction hash for the split transaction for the trasnaction
# above.
txid_bob_bcy_split = "407463857069c931ff4759ef565784468fb27999bc076653acc7f5b28d82ba9a"

# This is the secret used in this atomic swap.  It needs to be between 1 million
# and 2 billion.
atomic_swap_secret = 1076410890

# This function provides the pubKey script (aka output script) that will set
# up the atomic swap.  This function is run by both Alice (aka you) and Bob,
# but on different networks (tBTC for you/Alice, and BCY for Bob).  This is
# used to create TXNs 1 and 3, which are described at
# http://aaronbloomfield.github.io/ccc/slides/bitcoin.html#/xchainpt1.
def atomicswap_scriptPubKey(public_key_sender, public_key_recipient, hash_of_secret):
    return [ 
             OP_IF, OP_HASH160, hash_of_secret, OP_EQUALVERIFY, public_key_recipient, OP_CHECKSIG, OP_ELSE, public_key_sender, OP_CHECKSIGVERIFY, public_key_recipient, OP_CHECKSIG, OP_ENDIF
           ]

# This is the ScriptSig that the receiver will use to redeem coins.  It's
# provided in full so that you can write the atomicswap_scriptPubKey()
# function, above.  This creates the "normal" redeeming script, shown in steps 5 and 6 at 
# http://aaronbloomfield.github.io/ccc/slides/bitcoin.html#/atomicsteps.
def atomcswap_scriptSig_redeem(sig_recipient, secret):
    return [
        sig_recipient, secret, OP_TRUE,
    ]

# This is the ScriptSig for sending coins back to the sender if unredeemed; it
# is provided in full so that you can write the atomicswap_scriptPubKey()
# function, above.  This is used to create TXNs 2 and 4, which are
# described at
# http://aaronbloomfield.github.io/ccc/slides/bitcoin.html#/xchainpt1.  In
# practice, this would be time-locked in the future -- it would include a
# timestamp and call OP_CHECKLOCKTIMEVERIFY.  Because the time can not be
# known when the assignment is written, and as it will vary for each student,
# that part is omitted.
def atomcswap_scriptSig_refund(sig_sender, sig_recipient):
    return [
        sig_recipient, sig_sender, OP_FALSE,
    ]

# The transaction hash received after successfully submitting part 4a
txid_atomicswap_alice_send_tbtc = "450be3579c183679fd9c6130dc8e97fe1dc27e872e8c0b4c8b504a67494ba0a4"

# The transaction hash received after successfully submitting part 4b
txid_atomicswap_bob_send_bcy = "41c072e6a5994725fae35b7f17b37b832c74c344ec55d01782296e5f56662744"

# The transaction hash received after successfully submitting part 4c
txid_atomicswap_alice_redeem_bcy = "ccbeed04edce2022614b5fa48792dbf2b227f37af8831820655f3db1a3321a83"

# The transaction hash received after successfully submitting part 4d
txid_atomicswap_bob_redeem_tbtc = "f0b146d1de199def30a557305753de0213b14d330315da6a67f8e92c1e1eec4a"


#------------------------------------------------------------
# part 5: return everything to the faucet

# nothing to fill in here, as we are going to look at the balance of
# `my_invoice_address_str` to verify that you've completed this part.
