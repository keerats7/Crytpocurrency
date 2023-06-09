# Submission information for the Decentralized Exchange (DEX) HW
# https://aaronbloomfield.github.io/ccc/hws/dex/

# The filename of this file must be 'dex.py', else the submission
# verification routines will not work properly.

# You are welcome to have additional variables or fields in this file; you
# just cant remove variables or fields.


# Who are you?  Name and UVA userid.  The name can be in any human-readable format.
userid = "ks5hrx"
name = "Keerat Singh"


# eth.coinbase: this is the account that you deployed the smart contracts
# (and performed any necessary transactions) for this assignment.  Be sure to
# include the leading '0x' in the address.
eth_coinbase = "0x17d56256bbb6558970a31fb79ba6b02b73f2c8d5"


# This dictionary contains the contract addresses of the various contracts
# that need to be deployed for this assignment.  The addresses do not need to
# be in checksummed form.  The contracts do, however, need to be deployed by
# the eth_coinbase address, above.  Be sure to include the leading '0x' in
# the address.
contracts = {

	# The Token Cryptocurrency contract.  As you had to make a few changes,
	# you will have had to re-deploy it for this assignment.  The address
	# does not need to be in checksummed form.  It must have been deployed by
	# the eth_coinbase address, above.
	'token_cc': '0x19E44D5636f5Ee3d542691241B13Cf3f1967AE7f',

	# Your DEX contract.  All of the actions in this file are assumed to be
	# from this contract.  The address does not need to be in checksummed
	# form.  It must have been deployed by the eth_coinbase address, above.
	'dex': '0x01511475e579C20F32f71D9cA7176232e45b5b36',
}


# This dictionary contains various information that will vary depending on the
# assignment.
other = {
	
	# This is the transaction hash from when you called createPool() on the
	# deployed DEX, above, with exactly 100 ether and at least 10.0 TC
	'createpool_call_txn': '0x97f097afdf21ec9188af62a4d3cec2c4f7e83fd55a23073ea08684370ee4acab',

}


# These are various sanity checks, and are meant to help you ensure that you
# submitted everything that you are supposed to submit.  Other than
# submitting the necessary files to Gradescope (which checks for those
# files), all other submission requirements are listed herein.  These values
# need to be changed to True (instead of False).
sanity_checks = {
	
	# For the TokenCC that you are using for this assignment, did you make the
	# changes required in the DEX homework?  This is adding the
	# `_afterTokenTransfer()` function.
	'modified_tokencc': True,

	# Does the `symbol()` function in your DEX contract return the symbol for
	# your token cryptocurrency?
	'dex_symbol_returns_tcc_symbol': True,

	# Did you register your DEX with the course dex.php web page? This implies
	# that you deployed both TokenDEX and TokenCC to the private Ethereum
	# blockchain.
	'registered_dex_with_course_page': True,

	# Did you call createPool() on your DEX with *exactly* 100 (fake) ETH? 
	'called_createpoool_with_100_eth': True,

	# When you called createPool(), did you send in at least 10.0 of your TC?
	# You can use more, if you would like.
	'called_createpoool_with_10_or_more_tc': True,

	# Is your DEX initialized with the *variable* EtherPricer contract?
	'initialized_dex_with_variable_etherpriceoracle': True,

	# Did you send me exactly 10.0 of your token cryptocurrencty?  If your
	# token cryptocurrency uses 8 decimals, then that will be 1,000,000,000
	# total units sent.  This is from the TokenCC that you deployed in
	# the 'contracts' section, above.
	'sent_me_10_of_your_cc': True,

	# Did you, or will you, make 4 exchanges on somebody else's DEX?  These
	# bids are due 24 hours after the assignment due date
	'made_4_exchanges_on_other_dexes': True,

}


# While some of these are optional, you still have to replace those optional
# ones with the empty string (instead of None).
comments = {

	# How long did this assignment take, in hours?  Please format as an
	# integer or float.
	'time_taken': 8,

	# Any suggestions for how to improve this assignment?  This part is
	# completely optional.  If none, then you can have the value here be the
	# empty string (but not None).
	'suggestions': 'Try catch bug was really weird.',

	# Any other comments or feedback?  This part is completely optional. If
	# none, then you can have the value here be the empty string (but not
	# None).
	'comments': 'Fantastic assignment yet again.',
}
