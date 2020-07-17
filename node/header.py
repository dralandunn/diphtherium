# Module containing classes and parameters
#
import json

class transaction:
    # A structure to hold a single transaction consisting of
    # multiple inputs and multiple outputs
    #
    def __init__(self, inputs, outputs):
        # inputs is a list of tuples each referencing
        # a transaction on the Blockchain 
        #
        self.inputs = inputs
        self.outputs = outputs
        self.nVin = len(self.inputs)
        self.nVout = len(self.outputs)
        self.Vin = self.Vin(inputs)
        self.Vout = self.Vout(outputs)
        

    def Vin(self, inputs):
        # converts inputs list into dictionary
        Vin = []
        for t in inputs:
            Vin.append({"TxID":t[0],"index":t[1],"SigScript":t[2],"marker":0xfeffffff})
        return Vin
        
    def Vout(self,outputs):
        # converts outputs list to dictionary
        Vout = []
        for t in outputs:
            Vout.append({"CAmount": t[0],"PubKeyScript":t[1]})
        return Vout

        
    def fmt(self, fmt):
        # returns complete Tx in specified format
        # fmt = json
        # fmt = dict
        # fmt = byte
        # Build Tx as dictionary
        tx = {"version": 1,
              "nVin": self.nVin,
              "Vin": self.Vin,
              "nVout": self.nVout,
              "Vout": self.Vout,
              "Timelock": 234
             }
        
        if fmt=="dict":
            return tx
        elif fmt=="json":
            return json.dumps(tx)
        elif fmt=="byte":
            return
        return "error"

    def output(self, n):
        # returns nth output as dictionary
        if n<self.nVout:
            return self.Vout[n]
        else:
            return "Error: index out of bounds"

    
    def fees(self):
        # returns fees in satoshi (Int)
        #
        def getInputTotal():
            # Temporary until blockchain
            # is working
            total = 1.1*getOutputTotal()
            return total
        
        def getOutputTotal():
            # Sums the staoshi in all
            # of the TX outputs
            total = 0
            for t in self.Vout:
                total += t["CAmount"]
            return total
        
        fees = getInputTotal() - getOutputTotal()
        return fees
    

    def test(self):
        return self.Vout[0]["CAmount"]
#-----------------------------------------------------------------------------------
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


#------------------------------------------------------------------------------------
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

#TEST------------------------------------------------------------

#TxID, Index, SigScript
inputs = [(0xa1a1a1, 1, "a73e2fcc232"),
          (0x434ff, 1, "23bb2ba")
         ]

#CAmount, PubKeyScript
outputs = [(123, "aff45"),
           (672, "12a5d67")
          ]
#instantiate transaction class
Tx = transaction(inputs, outputs)

#print(Tx.nVin)
#print(Tx.nVout)
print(Tx.Vin)
print(Tx.Vout)
#print(Tx.fmt("dict"))
#print(Tx.fmt("json"))
#print(Tx.output(1))

#print(Tx.fees())
