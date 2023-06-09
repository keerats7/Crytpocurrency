#!/bin/bash

echo The name of this cryptocurrency is:
./cryptomoney.sh name
echo Creation of the genesis block
./cryptomoney.sh genesis
echo Creating a wallet for alice into alice.wallet.txt
./cryptomoney.sh generate alice.wallet.txt
export alice=`./cryptomoney.sh address alice.wallet.txt`
echo alice.wallet.txt wallet signature: $alice
echo funding alice wallet with 100
./cryptomoney.sh fund $alice 100 01-alice-funding.txt
echo Creating a wallet for bob into alice.wallet.txt
./cryptomoney.sh generate bob.wallet.txt
export bob=`./cryptomoney.sh address bob.wallet.txt`
echo bob.wallet.txt wallet signature: $bob
echo funding bob wallet with 100
./cryptomoney.sh fund $bob 100 02-bob-funding.txt
echo transfering 12 from alice to bob
./cryptomoney.sh transfer alice.wallet.txt $bob 12 03-alice-to-bob.txt
echo transfering 2 from bob to alice
./cryptomoney.sh transfer bob.wallet.txt $alice 2 04-bob-to-alice.txt
echo verifying the last four transactions
./cryptomoney.sh verify alice.wallet.txt 01-alice-funding.txt
./cryptomoney.sh verify bob.wallet.txt 02-bob-funding.txt
./cryptomoney.sh verify alice.wallet.txt 03-alice-to-bob.txt
./cryptomoney.sh verify bob.wallet.txt 04-bob-to-alice.txt
echo displaying the mempool
cat mempool.txt
echo checking the balance of both alice and bob
./cryptomoney.sh balance $alice
./cryptomoney.sh balance $bob
echo mining the block with prefix of 2
./cryptomoney.sh mine 2
sha256sum block_1.txt
echo validating the cryptocurrency chain
./cryptomoney.sh validate
echo carl incoming
./cryptomoney.sh generate carl.wallet.txt
export carl=`./cryptomoney.sh address carl.wallet.txt`
echo carl.wallet.txt wallet tag: $carl
echo give him 50 alice
./cryptomoney.sh transfer alice.wallet.txt $carl 50 05-alice-to-carl.txt
./cryptomoney.sh verify alice.wallet.txt 05-alice-to-carl.txt
./cryptomoney.sh balance $carl
./cryptomoney.sh mine 3
./cryptomoney.sh validate
echo carl wants to send more than he has
./cryptomoney.sh transfer carl.wallet.txt $bob 60 06-carl-to-bob.txt
./cryptomoney.sh balance $carl 
./cryptomoney.sh verify carl.wallet.txt 06-carl-to-bob.txt
alice has 40, bob has 110, carl has 50
./cryptomoney.sh balance $alice
./cryptomoney.sh balance $bob
./cryptomoney.sh balance $carl
echo carl gives bob 50, bob gives alice 40, carl gives alice 10, alice gives carl 30
./cryptomoney.sh transfer carl.wallet.txt $bob 50 07-carl-to-bob.txt
./cryptomoney.sh verify carl.wallet.txt 07-carl-to-bob.txt
./cryptomoney.sh transfer bob.wallet.txt $alice 40 08-bob-to-alice.txt
./cryptomoney.sh verify bob.wallet.txt 08-bob-to-alice.txt
./cryptomoney.sh transfer carl.wallet.txt $alice 10 09-carl-to-alice.txt
./cryptomoney.sh verify carl.wallet.txt 09-carl-to-alice.txt
./cryptomoney.sh transfer alice.wallet.txt $carl 30 10-alice-to-carl.txt
./cryptomoney.sh verify alice.wallet.txt 10-alice-to-carl.txt
./cryptomoney.sh balance $alice
./cryptomoney.sh balance $bob
./cryptomoney.sh balance $carl
