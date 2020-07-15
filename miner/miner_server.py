from hashlib import sha256
import time
import json
import threading
import logging
import requests
from flask import Flask, request

##INITIALIZATION-----------------------------------------------
# Registered Node
CONNECTED_NODE_ADDRESS = "http://192.168.1.20:8000"

# Number of satoshi in 1 BTC
COIN = 100000000

#Difficulty in Bitcoin floating point format
# e.g.0x0404cb1e takes 13.6 seconds
bits = 0x0404cb1e

# In early versions of Bitcoin the nonce was
# allocated four 8-bit bytes in the header.
max_nonce = 2 ** 32
        
app = Flask(__name__)

logging.basicConfig(filename='miner.log',
                    filemode='w',
                    format='(%(threadName)-9s) %(message)s',
                    level=logging.DEBUG)


## Mining Functions---------------------------------------------

def valid_Blk(blk):
    # Checks hash on mined block
    return True
 
def getblocktemplate(): 
    # WORKING
    # request data from Node to build candidate block
    # data returned as json object
    try:
        newBlockData = requests.get(CONNECTED_NODE_ADDRESS + "/getblocktemplate")
    except:
        newBlockData = {'error':'HTTP'}
        app.logger.debug('getBlockTemplate error')
        
    return newBlockData.json()

def selectUTXO(mempool):
    # From downloaded mempool select Tx to mine
    # based on:
    # - space is reserved for High priority Tx see p.185
    # - max fee/kB size
    # - total size must not exceed MAX_BLOCK_SIZE
    # - currently just selects the first 4
    #
    minTx = 2
    maxTx = 4
    
    # Number of unconfirmed Tx in pool
    nuTx = len(mempool)
    
    if nuTx >maxTx:
        #select first four Tx
        selTx = mempool[:4]
    else:
        selTx = mempool
        
    return selTx
## End selectUTX---------------------------------------------------

def buildBlock(selTx):
    # Builds new Candidate block
    # calculates Merkle Tree for transactions
    # builds header
    #

    def Merkle(selTx):
        MerkleRoot = "5e049f4030e0ab2debb92378f53c0a6e09548aea083f3ab25e1d94ea1155e29d"
        return MerkleRoot

    def getBlockValue(nHeight, nFees):
        # Reward for mining new block
        # reduces with time, but
        # here a constant
        nSubsidy = 6.25 * COIN
        return reward
    
    def sumFees(Tx):
        fee = 0
        for t in Tx:
            fee = int(["fee"])
        return fee
    
    # Construct coinbase transaction
    # Creates new bitcoin and pays it to miner
    CoinBase = {"version" : 1,
                "nInputs" : 1,
                "inputs" : [
                    {"hash" : "",
                     "index" : "ffffffff",
                     "ScriptBytes" : 200,
                     "height" : "22750",
                     "script" : "xxxx...",
                     "sequence" : 0
                    }
                    ],
                "nOutputs" : 1,
                 "outputs" : [
                     {"amount" : 4500,
                      "P2PKH" : "OP_DUP OP_HASH160 <PubKeyHash> OP_EQUALVERIFY OP_CHECKSIG",
                      "nLockTime" : 0
                      }
                     ]
               }
    
    # Generate new public key to receive payment
    newPubKey = "ddd"

    # Payment amount
    reward = getBlockValue(2765, sumFees(selTx))

    # Assemble new canditate block and return
    Blk = {
           "hdr" : {"Version":1,
                   "hashPrevBlock":"00000000000000027e7ba6fe7bad39faf3b5a83daed765f05f7d1b71a1632249",
                   "hashMerkleRoot":MerkleRoot(selTx),
                   "time":int(time.time()),
                   "bits":4,
                   "nonce":0,
                   },
           "NTx":len(selTx),
           "Tx": selTX
          }
    return Blk
## End buildBlk -------------------------------------------------------------------

# Mine block
def mineBlock(candidate):
    # Mine block

    def computed_hash(hdr):
        return
    
    def proof_of_work(hdr, bits):
        """
        Function increments values of nonce until the hash of header
        starts with the number of zeros defined by difficulty.
        """
        # calculate the difficulty target
        # - the number that the hash must be less than
        coeff = bits >> 8
        exp = bits & 0xff
        target = coeff *(2**(8*(exp - 3)))
 
        for nonce in range(max_nonce):
            hdr["nonce"] = nonce
            uHeader = str(header).encode('utf-8')
            hash_result = hashlib.sha256(uHeader).hexdigest()
        
        # check if this is a valid result
        # i.e. below the target
        if int(hash_result,16) < target:
            #print('Success with nonce {}'.format(nonce))
            #print('Hash is {}'.format(hash_result))
            return (hash_result,nonce)

        print('Failed after {} tries'.format(max_nonce))
        return nonce
    
    header = candidate["header"]
    candidate["header"] = proof_of_work(header, bits)
   
    return candidate



def Broadcast():
    # Broadcast NewBlock
    return


##MAIN------------------------------------------------------------
# This program runs continuously in two threads.
# Thread 1 listens to see if any other miner has completed a block
# Thread 2 performs the following functions:
#          a. Gets list of unconfirmed transactions from node
#          b. Selects suitable transactions to mine
#          C. builds a block
#          d. Mines the block
#          e. If successful, broadcasts new block to node(s)
#
# If the listner on Thread 1 receives a message that a new block
# has been completed by another miner, it first verifies the new block
# and sends a confirmation, and then flags this to Thread 2
# and the process begins again at step a.
#
def listener(e):                   
    """
    Listens for network broadcasts
    If new block is broadcast, Flag e is set
    and mining restarts
    """
    @app.route('/newblk', methods=['POST'])
    def new_blk():
        # ENDPOINT for new block broadcast message (Thread 1)
        # new block is retained as base for next block
        # need to remember its hash and height
        def is_valid_proof(cls, block, block_hash):
            """
            Check if block_hash is a valid hash of block and satisfies
            the difficulty criteria.
            """
            return (block_hash.startswith('0' * Blockchain.difficulty) and block_hash == block.compute_hash())

        def is_standard_tx():
            """
            Checks to see if Tx is one of 5 types:
              - Pay-to-Public-Key-Hash (P2PKH)
              - Public-Key
              - Multi-Signature (limited to 15 keys)
              - Pay-to-Script-Hash (P2SH)
              - Data Output (OP_RETURN)
            """
            return True

        app.logger.debug('Listening')
        
        # Get transaction as json string and
        # convert to a dictionary object
        # Blk_json = request.get_json()
        # block = json.loads(Blk_json)
        # cls = 5
        # block_hash = "2345"
  
        if True:
            #is_standard() and is_valid_proof(cls, block, block_hash):
            # Set Flag to stop mining
            e.set()
            app.logger.debug('Block Valid: stop mining')
            RESPONSE = "confirmed"
        else:
            RESPONSE = "confirmed"
            app.logger.debug('Block Invalid')
        return RESPONSE

def miner(e):
    # Main mining module (Thread 2)
    app.logger.debug('Mining')
    n=0
    while n<100:
        n += 1
        try:
            if e.isSet(): raise Exception()
            
            # Get new block data from Node
            # newBlkData is a json object
            newBlkData = getblocktemplate()
            app.logger.debug('Received newBlkData')
            
            # Select Tx to mine
            selTx = selectUTXO(newBlkData)
            app.logger.debug('Tx selected %s', selTx)
            
            # Build block from header and Tx
            candidate = buildBlock(selTx, newBlkData)
            app.logger.debug('Candidate block built ')
            
            # Mine block
            hdr = candidate["hdr"]
            newBlk = mineBlock(hdr, bits)
            app.logger.debug('Block mined ')
            
            # Broadcast NewBlock
            Broadcast(newBlk)
            app.logger.debug('Block broadcast ')

        except:
            # clear flag and restart mining
            app.logger.debug('Restart Mining')
            e.clear()


if True:
    #__name__ == '__main__':
    # Listner raise flag when another miner completes
    # a block. Sends signal to other thread to restart mining
    e = threading.Event()

    # Thread for Block Miner
    t1 = threading.Thread(name='miner', target=miner, args=(e,))

    # Spawn daemon thread for listener
    t2 = threading.Thread(name='listener', target=listener, args=(e,))
    t2.setDaemon(True)

    t1.start()
    app.logger.info('Started Miner')
    
    t2.start()
    app.logger.info('Spawned Listener')

    app.run(debug=True)
