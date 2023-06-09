import sys
import json
import datetime
from hashlib import sha256

def reverse_endianess(hex_str):
    rev_hex_str = ''
    i = len(hex_str)
    while i > 0:
        rev_hex_str += hex_str[i-2:i]
        i -= 2
    return rev_hex_str
def num_bytes_csuint(size_byte):
    num_bytes_used = 1
    offset = 0 #if more than 1 byte, actual number is stored after signal byte for csuint
    if size_byte == 253:
        num_bytes_used = 3
        offset = 1
    elif size_byte == 254:
        num_bytes_used = 5
        offset = 1
    elif size_byte == 255:
        num_bytes_used = 9
        offset = 1
    return num_bytes_used, offset

def parse_transaction_in(transaction_bytes, start_byte, output_json, transaction_num, block_num):
    TXID_hash = transaction_bytes[start_byte:start_byte + 32]
    index = transaction_bytes[start_byte + 32:start_byte + 36]
    in_script_size_byte = transaction_bytes[start_byte + 36]
    in_script_num_bytes_used, offset = num_bytes_csuint(in_script_size_byte)
    in_script_size = transaction_bytes[start_byte + 36 + offset:start_byte + 36 + in_script_num_bytes_used]
    in_script_start_byte = start_byte + 36 + in_script_num_bytes_used
    in_script_end_byte = in_script_start_byte + int.from_bytes(in_script_size, 'little')
    in_script = transaction_bytes[in_script_start_byte:in_script_end_byte]
    seq_num = transaction_bytes[in_script_end_byte:in_script_end_byte + 4]
    output_json["blocks"][block_num]["transactions"][transaction_num]["txn_inputs"].append({"utxo_hash": reverse_endianess(TXID_hash.hex()),
                                                                                                "index": int.from_bytes(index, 'little'),
                                                                                                "input_script_size": int.from_bytes(in_script_size, 'little'),
                                                                                                "input_script_bytes": in_script.hex(),
                                                                                                "sequence": int.from_bytes(seq_num, 'little')
                                                                                                })
    return in_script_end_byte + 4, output_json
def parse_transaction_out(transaction_bytes, start_byte, output_json, transaction_num, block_num):
    value = transaction_bytes[start_byte:start_byte + 8]
    #print("value: ", int.from_bytes(value, 'little'))
    out_script_size_byte = transaction_bytes[start_byte + 8]
    out_script_num_bytes_used, offset = num_bytes_csuint(out_script_size_byte)
    out_script_size = transaction_bytes[start_byte + 8 + offset:start_byte + 8 + out_script_num_bytes_used]
    out_script_start_byte = start_byte + 8 + out_script_num_bytes_used
    out_script_end_byte = out_script_start_byte + int.from_bytes(out_script_size, 'little')
    out_script = transaction_bytes[out_script_start_byte:out_script_end_byte]
    output_json["blocks"][block_num]["transactions"][transaction_num]["txn_outputs"].append({"satoshis": int.from_bytes(value, 'little'),
                                                                                                "output_script_size": int.from_bytes(out_script_size, 'little'),
                                                                                                "output_script_bytes": out_script.hex()
                                                                                                })
    return out_script_end_byte, output_json
def parse_transaction(transaction_bytes, start_byte, output_json, transaction_num, block_num):
    #version
    version = transaction_bytes[start_byte:start_byte + 4]
    if version != b'\x01\x00\x00\x00':
        #Error 4: Invalid transaction version number
        print("error {} block {}".format(5, block_num))
        exit()
    #tx_in_count, tx_in
    txn_in_count_size_byte = transaction_bytes[start_byte + 4]
    txn_in_count_num_bytes_used, offset = num_bytes_csuint(txn_in_count_size_byte)
    txn_in_count = transaction_bytes[start_byte + 4 + offset:start_byte + 4 + txn_in_count_num_bytes_used]
    #print("transac in: ", int.from_bytes(txn_in_count, 'little'))
    start_transaction_in_i = start_byte + 4 + txn_in_count_num_bytes_used
    output_json["blocks"][block_num]["transactions"][transaction_num]["version"] = int.from_bytes(version, 'little')
    output_json["blocks"][block_num]["transactions"][transaction_num]["txn_in_count"] = int.from_bytes(txn_in_count, 'little')
    for i in range(int.from_bytes(txn_in_count, 'little')):
        #print("transac in {} starts at byte {}".format(i, start_transaction_in_i))
        start_transaction_in_i, output_json = parse_transaction_in(transaction_bytes, start_transaction_in_i, output_json, transaction_num, block_num)
    #txn_out_count, txn_out
    txn_out_count_size_byte = transaction_bytes[start_transaction_in_i]
    txn_out_count_num_bytes_used, offset = num_bytes_csuint(txn_out_count_size_byte)
    txn_out_count = transaction_bytes[start_transaction_in_i + offset:start_transaction_in_i + txn_out_count_num_bytes_used]
    #print("transac out: ", int.from_bytes(txn_out_count, 'little'))
    start_transaction_out_i = start_transaction_in_i + txn_out_count_num_bytes_used
    output_json["blocks"][block_num]["transactions"][transaction_num]["txn_out_count"] = int.from_bytes(txn_out_count, 'little')
    for i in range(int.from_bytes(txn_out_count, 'little')):
        #print("transac out {} starts at byte {}".format(i, start_transaction_out_i))
        start_transaction_out_i, output_json = parse_transaction_out(transaction_bytes, start_transaction_out_i, output_json, transaction_num, block_num)
    #lock_time
    lock_time = transaction_bytes[start_transaction_out_i:start_transaction_out_i+4]
    output_json["blocks"][block_num]["transactions"][transaction_num]["lock_time"] = int.from_bytes(lock_time, 'little')
    return start_transaction_out_i+4, output_json
    

def parse_header(header_bytes, actual_prev_block_hash, prev_block_timestamp, actual_merkle_root_hash, output_json, block_num):
    version = header_bytes[0:4] # 4 bytes
    prev_block_hash = header_bytes[4:36] # 32 bytes sha256(sha256(prev_block_header))
    merkle_root_hash = header_bytes[36:68] # 32 bytes
    time_bytes = header_bytes[68:72] # 4 bytes
    cur_block_timestamp = datetime.datetime(1970,1,1) + datetime.timedelta(int.from_bytes(time_bytes, 'little') / (60 * 60 * 24))
    nBits = header_bytes[72:76] # 4 bytes
    nonce = header_bytes[76:80] # 4 bytes
    if version != b'\x01\x00\x00\x00':
        #Error 2: Invalid block header version number
        print("error {} block {}".format(2, block_num))
        exit()
    if block_num != 0 and prev_block_hash != actual_prev_block_hash:
        #Error 3: Invalid prev_block_hash (not including genesis block)
        print("error {} block {}".format(3, block_num))
        exit()
    if block_num != 0 and cur_block_timestamp - prev_block_timestamp < datetime.timedelta(hours=-2):
        #Error 4: timestamp of current block needs to be no earlier than 2 hours after timestamp of prev_block (not including genesis block)
        print("error {} block {}".format(4, block_num))
        exit()
    if merkle_root_hash != actual_merkle_root_hash:
        #Error 6: Invalid merkle root hash
        print("error {} block {}".format(6, block_num))
        exit()
    output_json["blocks"][block_num]["version"] = int.from_bytes(version, 'little')
    output_json["blocks"][block_num]["previous_hash"] = reverse_endianess(prev_block_hash.hex())
    output_json["blocks"][block_num]["merkle_hash"] = reverse_endianess(merkle_root_hash.hex())
    output_json["blocks"][block_num]["timestamp"] = int.from_bytes(time_bytes, 'little')
    output_json["blocks"][block_num]["timestamp_readable"] = cur_block_timestamp
    output_json["blocks"][block_num]["nbits"] = reverse_endianess(nBits.hex())
    output_json["blocks"][block_num]["nonce"] = int.from_bytes(nonce, 'little')
    return cur_block_timestamp, output_json

def parse_block(magic_number_bytes, block_size_bytes, content_bytes, actual_prev_block_hash, prev_block_timestamp, output_json, block_num):
    if magic_number_bytes != b'\xf9\xbe\xb4\xd9':
        #Error 1: invalid magic number
        print("error {} block {}".format(1, block_num))
        exit()
    header_bytes = content_bytes[0:80]
    txn_count_size_byte = content_bytes[80]
    txn_count_num_bytes_used, offset = num_bytes_csuint(txn_count_size_byte)
    txn_count = content_bytes[80+offset:80 + txn_count_num_bytes_used]
    #print("num transac: ", int.from_bytes(txn_count, 'little'))
    output_json["blocks"][block_num]["txn_count"] = int.from_bytes(txn_count, 'little')
    merkle_hashes = []
    #txn_count transactions will follow, each of varying size...
    start_next_transaction = 80 + txn_count_num_bytes_used
    for i in range(int.from_bytes(txn_count, 'little')):
        #print("transac {} starts at byte {}".format(i, start_transaction_i))
        start_transaction_i = start_next_transaction
        output_json["blocks"][block_num]["transactions"].append({"version": 1,
                                                                    "txn_in_count": None,
                                                                    "txn_inputs": [],
                                                                    "txn_out_count": None,
                                                                    "txn_outputs": [],
                                                                    "lock_time": None
                                                                    })
        start_next_transaction, output_json = parse_transaction(content_bytes, start_next_transaction, output_json, i, block_num)
        end_transaction_i = start_next_transaction
        merkle_hashes.append(sha256(sha256(content_bytes[start_transaction_i:end_transaction_i]).digest()).digest()) #merkle_hashes: sha(sha(transaction))
    cur_block_hash = sha256(sha256(header_bytes).digest()).digest() #cur_block_hash: sha(sha(header))
    #verify merkle root:
    while len(merkle_hashes) > 1:
        temp = []
        for i in range(0, len(merkle_hashes), 2):
            concat_hash = merkle_hashes[i]
            if i + 1 < len(merkle_hashes):
                concat_hash += merkle_hashes[i+1]
            else:
                concat_hash += merkle_hashes[i]
            temp.append(sha256(sha256(concat_hash).digest()).digest())
        merkle_hashes = temp
    cur_block_timestamp, output_json = parse_header(header_bytes, actual_prev_block_hash, prev_block_timestamp, merkle_hashes[0], output_json, block_num)
    return cur_block_hash, cur_block_timestamp, output_json

def parse_blocks(block_file):
    magic_number = []
    block_size = []
    content = []
    block_num = 0
    loc = 0
    actual_prev_block_hash = b"Genesis" #Stored as bytes object LE
    prev_block_timestamp = datetime.datetime(1970, 1, 1) #Stored as datetime object
    output_json = {"blocks": [], "height": block_num}
    with open(block_file, 'rb') as f:
        incomplete_file = True
        while(b := f.read(1)):
            # read magic number, block_size, and block content
            # then move on to next block
            if loc == 4:
                magic_number_bytes = b"".join(magic_number)
                magic_number = []
            elif loc == 8:
                block_size_bytes = b"".join(block_size)
                block_size = []
            #Iterate byte-by-byte, process at end, reset at 8 + block_size for next block
            if loc < 4:
                magic_number.append(b)
            elif loc >=4 and loc < 8:
                block_size.append(b)
            elif loc >= 8 and loc < 8 + int.from_bytes(block_size_bytes, 'little'):
                content.append(b)
            loc += 1
            if loc > 8:
                if loc == 8 + int.from_bytes(block_size_bytes, 'little'):
                    content_bytes = b"".join(content)
                    #The height of the first block in the file should be displayed as 0, even if it is not the genesis block
                    output_json["blocks"].append({"height": block_num, 
                                                    "file_position": block_num, 
                                                    "version": None,
                                                    "previous_hash": None,
                                                    "merkle_hash": None,
                                                    "timestamp": None,
                                                    "timestamp_readable": None,
                                                    "nbits": None,
                                                    "nonce": None,
                                                    "txn_count": None,
                                                    "transactions": []
                                                    })
                    actual_prev_block_hash, prev_block_timestamp, output_json = parse_block(magic_number_bytes, block_size_bytes, content_bytes, actual_prev_block_hash, prev_block_timestamp, output_json, block_num)
                    content = []
                    loc = 0
                    block_num += 1
    output_json["height"] = block_num
    with open(block_file + ".json", "w") as f:
        f.write(json.dumps(output_json, default=str))
    print("no errors {} blocks".format(block_num))
if __name__ == '__main__':
    parse_blocks(sys.argv[1])