# Submission information for the Ethereum Tokens HW
# https://aaronbloomfield.github.io/ccc/hws/tokens/

# The filename of this file must be 'tokens.py', else the submission
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

	# The Token cryptocurrency (aka ERC-20) contract.  All of the token
	# cryptocurrencty transactions below are assumed to come from this
	# contract. The address does not need to be in checksummed form.  It must
	# have been deployed by the eth_coinbase address, above.
	'token_cc': "0x35D39A722Ea71ad60D54967BBdc0eF6188054b0A",

	# The NFT Manager (aka ERC-721) contract.  Two of the minted NFTs, below,
	# are assumed to come from this contract (the third comes from the
	# course-wide contract).  The address does not need to be in checksummed
	# form.  It must have been deployed by the eth_coinbase address, above.
	'nft_manager': '0x6CDfBd551Dd237E9523f1F3978D9EbC45b3B4307',
}


# This dictionary contains various information that will vary depending on the
# assignment.
other = {
	
	# This is the name of your cryptocurrency.  Be creative!  But don't use
	# something that will get me in trouble.  This can have any printable
	# ASCII character (no emojis) and spaces.
	'cryptocurrency_name': "LoveLetters",

	# The abbreviation for your cryptocurrency: at most 4 letters.  And be
	# sure it is not already used (see the assignment for how to verify this).
	'cryptocurrency_abbrev': "LOVE",

	# The transaction hash where you sent me 10.0 of your cryptocurrency.  It
	# must have been done by eth_coinbase, above.  And it must have used your
	# deployed TokenCC contract, above.
	'cc_sent_txn_hash': "0x22cb9f2b576f8822ab8cda3c816a0871dc5df8b616accff6240f8798cb9b7d15",

	# The NFT ID that you created from YOUR NFTManager (the nft_manager
	# contract, above) and kept (meaning you did not send to the course
	# instructor).  It must have been done by eth_coinbase, above.
	'nft_id_kept': 3,

	# The NFT ID that you sent to the course instructor from YOUR NFTManager
	# (the nft_manager contract, above).  It must have been done by
	# eth_coinbase, above.
	'nft_id_sent': 2,

	# The transaction hash where you sent me an NFT from YOUR NFTManager
	# (the nft_manager contract, above).  It must have been done by
	# eth_coinbase, above.  And it must have used your deployed NFTManager
	# contract, above.
	'nft_sent_txn_hash': "0x67ca2fd4d63080bde2f6ae465df853b86a4d0a093a63d56787c1839f98872d63",

	# The NFT ID from when you created an NFT on the course-wide NFT manager.
	# It must have been done by eth_coinbase, above.
	'course_nft_id': 48601030819304970751206378061506117314756414203890010921418646127557746884608,

	# The transaction hash from when you created an NFT on the course-wide NFT
	# manager.  It must have been done by eth_coinbase, above.
	'course_nft_txn_hash': "0x7eabe26d74776a8b7dda43f34fa2f10be3b17c6e64311cb4fad6da5c04349228",

}


# These are various sanity checks, and are meant to help you ensure that you
# submitted everything that you are supposed to submit.  Other than
# submitting the necessary files to Gradescope (which checks for those
# files), all other submission requirements are listed herein.  These values
# need to be changed to True (instead of False).
sanity_checks = {
	
	# Is your cryptocurrency logo image correct?  It should be 512x512, a .png
	# file, generally circular in appearance, and with a transparent
	# background outside the coin, and a non-white background in the circle
	# of the coin (these requirements match the template that was provided,
	# other than the non-white background).
	'cc_logo_image_is_correct': True,

	# Is your cc logo named properly?  It should be 'abcd.png', where 'abcd'
	# is your cryptocurrency abbreviation.  The file name should be all lower
	# case.
	'cc_logo_name_is_correct': True,

	# Did you upload your cryptocurrency logo to the 'cclogos/' directory?
	'uploaded_cc_logo': True,

	# Did you mint at least 100 coins of your TokenCC?  Keep in mind that you
	# have to add a number of decimal places after the number of coins minted.
	'minted_at_least_100_coins': True,

	# Did you send me exactly 10.0 of your token cryptocurrencty?  If your
	# token cryptocurrency uses 8 decimals, then that will be 1,000,000,000
	# total units sent.
	'sent_ten_tc': True,

	# Does your `supportsInterface()` function in TokenCC return true for the
	# four interfaces?
	'tokencc_supportsInterface_is_correct': True,

	# Is your TokenCC contract opening line *exactly:*
	# `contract TokenCC is ITokenCC, ERC20 {`?
	'tokencc_opening_line_is_correct': True,

	# Did you upload three NFT images?  They must be either .jpg, .png,
	# or .webp images.
	'uploaded_three_nft_images': True,

	# Are all three NFT images no larger than 2000x2000?
	'nft_image_sizes_correct': True,

	# Did you name the images correctly?  The names should start with your
	# userid followed by a underscore, and have the appropriate image
	# extension.  All filenames must be strictly less than or equal to 32
	# characters in length.
	'image_files_named_correctly': True,

	# Can anybody mint an NFT?  Just make sure you don't require() that the
	# minter is the deployer, for example.
	'anybody_can_mint_nft': True,

	# Did you send me one of your NFTs?  Which one was specified in
	# the 'nft_id_sent' field in the 'other' dictionary, above.
	'sent_nft': True,

	# Does your `supportsInterface()` function in NFTManager return true for
	# the four interfaces?
	'nftmanager_supportsInterface_is_correct': True,

	# Is your NFTManager contract opening line *exactly:*
	# `contract NFTManager is INFTManager, ERC721 {`?
	'nftmanager_opening_line_is_correct': True,

	# Did you create a NFT on the course-wide NFT manager?  The NFT ID for this was put into the 
	'created_course_nft': True,

}


# While some of these are optional, you still have to replace those optional
# ones with the empty string (instead of None).
comments = {

	# How long did this assignment take, in hours?  Please format as an
	# integer or float.
	'time_taken': 3,

	# Any suggestions for how to improve this assignment?  This part is
	# completely optional.  If none, then you can have the value here be the
	# empty string (but not None).
	'suggestions': "",

	# Any other comments or feedback?  This part is completely optional. If
	# none, then you can have the value here be the empty string (but not
	# None).
	'comments': "Cool assignment",
}
