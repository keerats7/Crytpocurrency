import sys
import rsa
from datetime import datetime
import hashlib
from os import remove
from os import listdir
from os.path import isfile, join
import re

def checkSign(filename, statement):
    source_wallet = ''
    dest_wallet = ''
    amount = 0
    time = ''
    signature = ''
    with open(statement, 'r') as rf:
        for i, line in enumerate(rf):
            if i == 0:
                source_wallet = line[6:].rstrip()
            elif i == 1:
                dest_wallet = line[4:].rstrip()
            elif i == 2:
                amount = int(line[8:].rstrip())
            elif i == 3:
                time = line[6:].rstrip()
            else:
                signature = line
    rf.close()
    source_pubkey, source_privkey = loadWallet(filename)
    msg = source_wallet + dest_wallet + str(amount) + time
    #hash1 = hashlib.sha256(message.encode()).hexdigest()
    hash1 = int.from_bytes(hashlib.sha256(msg.encode()).digest(), byteorder='big')
    signature = pow(hash1, source_privkey['d'], source_privkey['n']) #Signed with source private key
    hash2 = pow(signature, source_pubkey['e'], source_pubkey['n'])
    print(msg)
    print(hash1)
    print(signature)
    print(hash2)
    return 0


def loadWallet(filename):
    with open(filename, mode='rb') as file:
        keydata = file.read()
    privkey = rsa.PrivateKey.load_pkcs1(keydata)
    pubkey = rsa.PublicKey.load_pkcs1(keydata)
    return pubkey, privkey

def hashFile(filename):
    # gets the hash of a file; from https://stackoverflow.com/a/44873382
    h = hashlib.sha256()
    with open(filename, 'rb', buffering=0) as f:
        for b in iter(lambda : f.read(128*1024), b''):
            h.update(b)
    return h.hexdigest()

def getAddress(filename):
    start_char = 31
    tag_len = 16
    tag = ''
    with open(filename, 'r') as f:
        for line in f:  
            for ch in line:
                if start_char > 0:
                    start_char -= 1
                elif tag_len > 0:
                    tag += ch
                    tag_len -= 1
                else:
                    break
        f.close()
    return tag

def getBalance(wallet):
    block_files = [f for f in listdir('./') if isfile(join('./', f)) and (f == 'mempool.txt' or bool(re.search("block_.*\.txt", f)))]
    balance = 0
    for block in block_files:
        with open(block, 'r') as f:
            for line in f:
                if "Gently does it..." in line or "transferred" not in line or "Nonce" in line:
                    continue
                transferred_pos = str.find(line, "transferred")
                to_pos = str.find(line, "to")
                amount = int(line[transferred_pos + 12:to_pos - 1])
                sender = line[0:transferred_pos - 1]
                receiver = line[to_pos + 3: to_pos + 19]
                if sender == wallet:
                    #Transferred coins
                    balance -= amount
                elif receiver == wallet:
                    #Recieved coins
                    balance += amount
            f.close()
    return balance

def name():
    #Name of my cryptocurrency
    print('KeeratDollar')

def genesis():
    #Creates the genesis block for the block chain
    with open('block_0.txt', 'w') as f:
        f.write('Gently does it...')
        f.close()
    print('Gently does it...')

def generate(filename):
    (pubkey, privkey) = rsa.newkeys(1024)
    pubkey_text = pubkey.save_pkcs1().decode("utf-8")
    privkey_text = privkey.save_pkcs1().decode("utf-8")
    tag = pubkey_text[31:47]
    with open(filename, 'w') as f:
        f.write(pubkey_text)
        f.write(privkey_text)
        f.close()
    print('New wallet generated in {} with tag {}'.format(filename, tag))

def address(filename):
    print(getAddress(filename))
    return 0

def fund(dest_wallet, amount, statement):
    ultimate_source_wallet = 'Mr. Singh'
    time = str(datetime.now())
    with open(statement, 'w') as f:
        f.write("From: {}\n".format(ultimate_source_wallet))
        f.write("To: {}\n".format(dest_wallet))
        f.write("Amount: {}\n".format(amount))
        f.write("Date: {}\n".format(time))
        f.close()
    print('Funded wallet {} with {} KeeratDollars on {}'.format(dest_wallet, amount, time))

def transfer(source_filename, dest_wallet, amount, statement):
    source_wallet = getAddress(source_filename)
    source_privkey = loadWallet(source_filename)[1]
    time = str(datetime.now())
    with open(statement, 'w') as f:
        f.write("From: {}\n".format(source_wallet))
        f.write("To: {}\n".format(dest_wallet))
        f.write("Amount: {}\n".format(amount))
        f.write("Date: {}\n".format(time))
        f.close()
    hash = int.from_bytes(hashlib.sha256((source_wallet + dest_wallet + str(amount) + time).encode()).digest(), byteorder='big')
    signature = pow(hash, source_privkey['d'], source_privkey['n']) #Signed with source private key
    with open(statement, 'a') as f:
        f.write(hex(signature))
        f.close()
    print('Statement {}: transferred {} from {} to {} on {}'.format(statement, amount, source_filename, dest_wallet, time))

def balance(wallet):
    print(getBalance(wallet))
    return 0

def verify(filename, statement):
    source_wallet = ''
    dest_wallet = ''
    amount = 0
    time = ''
    signature = ''
    with open(statement, 'r') as rf:
        for i, line in enumerate(rf):
            if i == 0:
                source_wallet = line[6:].rstrip()
            elif i == 1:
                dest_wallet = line[4:].rstrip()
            elif i == 2:
                amount = int(line[8:].rstrip())
            elif i == 3:
                time = line[6:].rstrip()
            else:
                signature = line.rstrip()
    rf.close()
    #Check if from the ultimate source: Mr. Singh
    if source_wallet == "Mr. Singh":
        transaction_line = '{} transferred {} to {} on {}'.format(source_wallet, amount, dest_wallet, time)
        with open('mempool.txt', 'a') as f:
            f.write(transaction_line + "\n")
        print('The transaction in file {} with wallet {} is from Mr. Singh...yea, thats going to the mempool'.format(statement, filename))
        return True
    #Check signature (decrypt OG signature using source public key and compare hash from signature to hash from OG file)
    source_pubkey = loadWallet(filename)[0]
    hash_from_signature = pow(int(signature, 16), source_pubkey['e'], source_pubkey['n'])
    hash_from_file = int.from_bytes(hashlib.sha256((source_wallet + dest_wallet + str(amount) + time).encode()).digest(), byteorder='big')
    if hash_from_file != hash_from_signature:
        print(hash_from_file)
        print(hash_from_signature)
        print('The transaction in file {} with wallet {} is invalid due to not matching hashes'.format(statement, filename))
        return False
    #Check for enough funds
    if getBalance(source_wallet) < amount:
        print('The transaction in file {} with wallet {} is invalid due to insufficient funds'.format(statement, filename))
        return False
    #Valid transaction
    transaction_line = '{} transferred {} to {} on {}'.format(source_wallet, amount, dest_wallet, time)
    with open('mempool.txt', 'a') as f:
        f.write(transaction_line + "\n")
    print('The transaction in file {} with wallet {} is valid and was written to the mempool'.format(statement, filename))
    return True

def mine(difficulty):
    #difficulty will be the number of leading zeros to have in the hash value
    #Prepend to file: https://stackoverflow.com/questions/5914627/prepend-line-to-beginning-of-a-file
    prefix = ""
    for i in range(0, int(difficulty)):
        prefix += "0"
    i = 1
    for f in listdir('./'):
        if isfile(join('./', f)) and bool(re.search("block_.*\.txt", f)):
            a = str.find(f, '_') + 1
            b = str.find(f, '.')
            block_num = int(f[a:b])
            if block_num >= i:
                i = block_num + 1
    prev_block = "block_{}.txt".format(i-1)
    prev_block_hash = hashFile(prev_block)
    cur_block = "block_{}.txt".format(i)
    with open('pending-mining.txt', 'w') as wf:
        wf.write(prev_block_hash + "\n")
        with open('mempool.txt', 'r') as rf:
            wf.write(rf.read())
        rf.close()
    wf.close()
    nonce = 0
    while True:
        with open(cur_block, 'w') as wf:
            with open('pending-mining.txt', 'r') as rf:
                wf.write(rf.read())
                wf.write("Nonce: " + str(nonce))
            rf.close()
        wf.close()
        if hashFile(cur_block)[0:int(difficulty)] == prefix:
            break
        else:
            nonce += 1
    #cur_block is set, clear mempool.txt
    remove('mempool.txt')
    remove('pending-mining.txt')
    print("Mempool transactions moved to {} and mined with difficulty {} and nonce {}".format(cur_block, difficulty, nonce))
    return 0

def validate():
    num_blocks = 1
    valid = True
    for f in listdir('./'):
        if isfile(join('./', f)) and bool(re.search("block_.*\.txt", f)):
            a = str.find(f, '_') + 1
            b = str.find(f, '.')
            num_blocks = max(num_blocks, int(f[a:b]) + 1)
    for i in range(0, num_blocks - 1):
        #Check that block i + 1 contains the correct hash of block i
        hash_block_i = hashFile("block_{}.txt".format(i))
        hash = ''
        with open("block_{}.txt".format(i + 1), 'r') as f:
            hash = f.readline().rstrip()
            f.close()
        if hash != hash_block_i:
            valid = False
    print(valid)
    return valid

if __name__ == '__main__':
    if sys.argv[1] == 'name' or sys.argv[1] == 'genesis' or sys.argv[1] == 'validate':
        #0-arg functions
        globals()[sys.argv[1]]()
    elif sys.argv[1] == 'generate' or sys.argv[1] == 'address' or sys.argv[1] == 'balance' or sys.argv[1] == 'mine' or sys.argv[1] == 'hashFile':
        globals()[sys.argv[1]](sys.argv[2])
    elif sys.argv[1] == 'verify' or sys.argv[1] == 'checkSign':
        globals()[sys.argv[1]](sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'fund':
        globals()[sys.argv[1]](sys.argv[2], sys.argv[3], sys.argv[4])
    elif sys.argv[1] == 'transfer':
        globals()[sys.argv[1]](sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])