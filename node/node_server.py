from hashlib import sha256
import time
import json
import sqlite3
import requests
from flask import Flask, request


class Block:
    def __init__(self, index, transactions, timestamp, previous_hash, nonce=0):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce

    def compute_hash(self):
        """
        A function that return the hash of the block contents.
        """
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()


class Blockchain:
    # difficulty of our PoW algorithm
    difficulty = 2

    def __init__(self):
        self.unconfirmed_transactions = []
        self.chain = []

    def create_genesis_block(self):
        """
        A function to generate genesis block and appends it to
        the chain. The block has index 0, previous_hash as 0, and
        a valid hash.
        """
        genesis_block = Block(0, [], 0, "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    @property
    def last_block(self):
        return self.chain[-1]

    def add_block(self, block, proof):
        """
        A function that adds the block to the chain after verification.
        Verification includes:
        * Checking if the proof is valid.
        * The previous_hash referred in the block and the hash of latest block
          in the chain match.
        """
        previous_hash = self.last_block.hash

        if previous_hash != block.previous_hash:
            return False

        if not Blockchain.is_valid_proof(block, proof):
            return False

        block.hash = proof
        self.chain.append(block)
        return True

    @staticmethod
    def proof_of_work(block):
        """
        Function that tries different values of nonce to get a hash
        that satisfies our difficulty criteria.
        """
        block.nonce = 0

        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()

        return computed_hash

    def add_new_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)

    @classmethod
    def is_valid_proof(cls, block, block_hash):
        """
        Check if block_hash is valid hash of block and satisfies
        the difficulty criteria.
        """
        return (block_hash.startswith('0' * Blockchain.difficulty) and
                block_hash == block.compute_hash())

    @classmethod
    def check_chain_validity(cls, chain):
        result = True
        previous_hash = "0"

        for block in chain:
            block_hash = block.hash
            # remove the hash field to recompute the hash again
            # using `compute_hash` method.
            delattr(block, "hash")

            if not cls.is_valid_proof(block, block_hash) or \
                    previous_hash != block.previous_hash:
                result = False
                break

            block.hash, previous_hash = block_hash, block_hash

        return result



#==============================================================================
        
app = Flask(__name__)

# the node's copy of blockchain
blockchain = Blockchain()
blockchain.create_genesis_block()

# the address of other participating members of the network
peers = set()

## WORKING----------------------------------------------------------------
#  ENPOINT to receive a new transaction. Unconfirmed TXs are first validated
# and then added to the MEMPOOL where they wait to be selected
# for processing by a Mining Node.
#
@app.route('/tx', methods=['POST'])
def new_transaction():

    def create_connection(db_file):
        """
        connection to the SQLite database
        """
        print("dbFile: ", db_file, type(db_file))
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            print("Connected to Node database")
        except Error as e:
            print(e)
        return conn

    def tx2mempool(uTx):
        # Adds new unconfirmed Tx to mempool
        # uTx is a tuple
        # The MEMPOOL is stored in the
        # mempool table of node.db
        
        # create a connection db object
        dbPath = 'C:/Block_Node/node.db'
        conn = create_connection(dbPath)

        # create a cursor object
        c = conn.cursor()
                     
        c.execute("INSERT INTO mempool(TimeStamp, payee, label, amount, fee) VALUES(?, ?, ?, ?, ?)", uTx)
   
        # commit insert and close connection
        conn.commit()
        conn.close()
        
        return
    
    def valid_tx(tx):
        # tx is a dictionary object
        # returns true if:
        #   * all required fields are present
        #   * Tx size less than MAX_BLOCK_SIZE
        #   * Output greater than 0, less than 21 m BTC 
        #   * not coin base TX ie hash=0 N=-1
        #   * nLockTime <= INT_MAX
        #   * Tx size < 100 bytes
        #   * for each input find referenced output in chain or mempool
        #   * see mastering Bitcoin p.182 for complete set
        required_fields = ["timestamp", "payee", "label", "amount", "fee"]
        for field in required_fields:
            if not field in tx:
                return False
        return True
    
    ##Main uTx Handler
    # Get transaction as json string and
    # convert to a dictionary object
    tx_json = request.get_json()
    tx_data = json.loads(tx_json)
   
    if valid_tx(tx_data):
        # Covert Tx_data values to a tuple and store in MEMPOOL
        uTx = tuple(tx_data[k] for k in tx_data.keys())
        tx2mempool(uTx)
    else:
        print("Invalid transaction data", 404)

    return "Success", 201


## WORKING------------------------------------------------------------------------
#  ENDPOINT to return data required to mine new block
# 
@app.route('/getblocktemplate', methods=['POST', 'GET'])
def get_pending_tx():
    # Get uTx from node.db mempool table
    # and build a JASON obbject to return
#-----------------------------    
    def create_connection(db_file):
        """
        connection to the SQLite database
        """
        print("dbFile: ", db_file, type(db_file))
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            print("Connected to Node database")
        except Error as e:
            print(e)
        return conn
#----------------------------
    def get_uTx():
        # Returns all unconfirmed transactions
        # from mempool as a list of tuples
    
        # create a connection object
        conn = create_connection('node.db')

        # create a cursor object
        c = conn.cursor()
    
        c.execute("SELECT * FROM mempool")
    
        uTx = c.fetchall()

        # Close the database connection
        c.close()
        return uTx
 #----------------------------------   
    uTx = get_uTx()

    # Convert list of tuples to dictionary
    L = []
    n = 1
    for tx in uTx:
        L.append({"timestamp":tx[0],
                  "payee":tx[1],
                  "label":tx[2],
                  "amount":tx[3],
                  "fee":tx[4]
                  })

    # Build getBlockTemplate data structure
    BlkData = {
               "version" : 1,
               "previousblockhash" : "xxxx",
               "transactions" : [
                                 {
                                  "data" : "xxxx",
                                  "txid" : "xxxx",
                                  "hash" : "xxxx",
                                  "fee" : 6.25,
                                  "weight" : 4
                                 },
                                ],
               "target" : "xxx",
               "sizelimit" : 100,
               "weightlimit" : 23,
               "bits" : "xxxxxxxx",
               "height" : 22678
}

    return json.dumps(L)

##-------------------------------------------------------------
# ENDPOINT to return the node's copy of the chain.
# Our application will be using this endpoint to query
# all the posts to display.
@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.__dict__)
    return json.dumps({"length": len(chain_data),
                       "chain": chain_data,
                       "peers": list(peers)})


##--------------------------------------------------------------
# Endpoint to request the node to mine the unconfirmed
# transactions (if any). We'll be using it to initiate
# a command to mine from our application itself.
@app.route('/mine', methods=['GET'])
def mine_unconfirmed_transactions():
    result = blockchain.mine()
    if not result:
        return "No transactions to mine"
    else:
        # Making sure we have the longest chain before announcing to the network
        chain_length = len(blockchain.chain)
        consensus()
        if chain_length == len(blockchain.chain):
            # announce the recently mined block to the network
            announce_new_block(blockchain.last_block)
        return "Block #{} is mined.".format(blockchain.last_block.index)

##----------------------------------------------------------------------
# Endpoint to add new peers to the network.
@app.route('/register_node', methods=['POST'])
def register_new_peers():
    node_address = request.get_json()["node_address"]
    if not node_address:
        return "Invalid data", 400

    # Add the node to the peer list
    peers.add(node_address)

    # Return the consensus blockchain to the newly registered node
    # so that he can sync
    return get_chain()


##-----------------------------------------------------------------------
@app.route('/register_with', methods=['POST'])
def register_with_existing_node():
    """
    Internally calls the `register_node` endpoint to
    register current node with the node specified in the
    request, and sync the blockchain as well as peer data.
    """
    node_address = request.get_json()["node_address"]
    if not node_address:
        return "Invalid data", 400

    data = {"node_address": request.host_url}
    headers = {'Content-Type': "application/json"}

    # Make a request to register with remote node and obtain information
    response = requests.post(node_address + "/register_node",
                             data=json.dumps(data), headers=headers)

    if response.status_code == 200:
        global blockchain
        global peers
        # update chain and the peers
        chain_dump = response.json()['chain']
        blockchain = create_chain_from_dump(chain_dump)
        peers.update(response.json()['peers'])
        return "Registration successful", 200
    else:
        # if something goes wrong, pass it on to the API response
        return response.content, response.status_code


def create_chain_from_dump(chain_dump):
    generated_blockchain = Blockchain()
    generated_blockchain.create_genesis_block()
    for idx, block_data in enumerate(chain_dump):
        if idx == 0:
            continue  # skip genesis block
        block = Block(block_data["index"],
                      block_data["transactions"],
                      block_data["timestamp"],
                      block_data["previous_hash"],
                      block_data["nonce"])
        proof = block_data['hash']
        added = generated_blockchain.add_block(block, proof)
        if not added:
            raise Exception("The chain dump is tampered!!")
    return generated_blockchain

##------------------------------------------------------------------------
# endpoint to add a block mined by someone else to
# the node's chain. The block is first verified by the node
# and then added to the chain.
@app.route('/add_block', methods=['POST'])
def verify_and_add_block():
    block_data = request.get_json()
    block = Block(block_data["index"],
                  block_data["transactions"],
                  block_data["timestamp"],
                  block_data["previous_hash"],
                  block_data["nonce"])

    proof = block_data['hash']
    added = blockchain.add_block(block, proof)

    if not added:
        return "The block was discarded by the node", 400

    return "Block added to the chain", 201




def consensus():
    """
    Our naive consnsus algorithm. If a longer valid chain is
    found, our chain is replaced with it.
    """
    global blockchain

    longest_chain = None
    current_len = len(blockchain.chain)

    for node in peers:
        response = requests.get('{}chain'.format(node))
        length = response.json()['length']
        chain = response.json()['chain']
        if length > current_len and blockchain.check_chain_validity(chain):
            current_len = length
            longest_chain = chain

    if longest_chain:
        blockchain = longest_chain
        return True

    return False


def announce_new_block(block):
    """
    A function to announce to the network once a block has been mined.
    Other blocks can simply verify the proof of work and add it to their
    respective chains.
    """
    for peer in peers:
        url = "{}add_block".format(peer)
        headers = {'Content-Type': "application/json"}
        requests.post(url,
                      data=json.dumps(block.__dict__, sort_keys=True),
                      headers=headers)

