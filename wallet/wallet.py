"""
Bitcoin Wallet

Alan Dunn    June 2020
"""
# import pybitcointools library
# import bitcoin
import hashlib
import datetime
import time
import json
import csv
import sqlite3
import requests
from flask import Flask, render_template, redirect, request

# The node with which the wallet interacts, there can be multiple
# such nodes as well.
CONNECTED_NODE_ADDRESS = "http://192.168.1.12:8000"

posts = []

# Seed for deterministic key generation
# 12 -24 random words [bip0039]
seed = "ax5dfdsgfg"

# KEY MANAGEMENT-------------------------------------------------------
# NOT WORKING
# Store key pairs in flat file

def Base58(Payload):
    # encode Payload
    # Add version number
    version = 0x00
    vPayload = version + Payload

    # Calculate checksum and append
    # First 4 bits of double hash
    checksum = hashlib.sha256(hashlib.sha256(vPayload))[4:]
    ###vPayload.append(checksum)
                              
    # Base58 Encode                         
                              
    return

def CheckBase58():
    # Check if valid

    return


def GetnewPrivKey():
    # Deterministic key generation using hash
    # of previous key as seed. Feed random string of bits
    # into SHA256
    # check < (1.158x10^77)-1

    # BC Generator Point secp256k1
    G = ""
    PrivKey = ""
    return PrivKey


def dumpprivkey():
    # Prints private key in base-58
    # Wallet Import Format (WIF),
    print()
    return


def GetnewPubKey(PrivKey, mode):
    # mode = 0 uncompressed
    # mode = 1 compressed
    PubK = ""
    return PubK


def Getnewaddress(PubK):
    # Generates new public key
    # stores key pair
    # Double hash > PubKHash

    # Base58Check + version
    bcAddress = ""
    return bcAddress


def deleteKeyPair():
    # delete once used to unlock a Tx

    return
#-------------------------------------------------------------------------------
def getKeys():
    # Read key-pairs from file
    path = 'c:\blockchain\key-pairs.dat'
    keyfile = open(path, 'r')
    keys = keyfile.readlines()
    keyfile.close()

    #convert to list of tuples <privK, pubK>
    
    return keys

# IBM code ----------------------------
def fetch_posts():
    """
    Function to fetch the chain from a blockchain node, parse the
    data and store it locally.
    """
    get_chain_address = "{}/chain".format(CONNECTED_NODE_ADDRESS)
    response = requests.get(get_chain_address)
    if response.status_code == 200:
        content = []
        chain = json.loads(response.content)
        for block in chain["chain"]:
            for tx in block["transactions"]:
                tx["index"] = block["index"]
                tx["hash"] = block["previous_hash"]
                content.append(tx)

        global posts
        posts = sorted(content, key=lambda k: k['timestamp'],
                       reverse=True)
#-----------------------------------------
# WORKING
def toSatoshi(amount, unit):
    # Converts amount <class str>
    # from any unit <class str>
    # to satoshi <class int>

    # trap any non-numeric input
    try:
        val = float(amount)
    except ValueError
        print("Error in amount")

    if unit=="btc":
            return int(val*100000000)
        elif unit=="mbtc":
            return = int(val*100000)
        elif unit=="ubtc":
            return = int(val*100)
        else:
            # No conversion as already in satoshi
            return = int(val)

# NOT USED---------------------------------------------------------
def displayTime(timestamp):
    # Internally timestamps are stored in Unix epoch time (int)
    # this function converts them to a readable format
    # for display
    return timestamp.strftime("%d-%b-%Y (%H:%M:%S)")



# END POINTS
# Home Page ------------------------------
# WORKING
app = Flask(__name__)

@app.route('/')
def index():
    # TEMP static values
    # need to be fetched
    available = 300
    pending = 20
    balance = available + pending

    # Display wallet balances on home page
    return render_template('index.html', 
                           title='Diphtherium Wallet',
                           available=available, 
                           pending=pending, 
                           balance=balance)

# Send -----------------------------------------------
# WORKING
@app.route('/send', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        #this block is only entered when the form is submitted

        # get current Unix time
        time = time.time()
        
        # Store POST data in variables
        payee = request.form.get('payee')
        label = request.form.get('label')
        amount = request.form.get('amount')
        unit = request.form.get('unit')
        fee = request.form.get('fee')

        # Convert ammount to satoshi
        satoshi = toSatoshi(amount, unut)
        
        # Build Transaction in dictionary
        TransData = {'timestamp':time,
                     'payee':payee,
                     'label':label,
                     'amount':satoshi,
                     'fee':fee}
        print(displayTime(time)
        
        # Convert dictionary to JSON Object for transmission
        TransJSON = json.dumps(TransData)
        
        # Post JSON object to Server Node
        res = requests.post(CONNECTED_NODE_ADDRESS + '/tx', json=TransJSON)
        #print(res)
        
        return render_template('send.html', title='Diphtherium Wallet')
    
    #if no post received, return empty form
    return render_template('send.html', title='Diphtherium Wallet')


# Receive------------------------------------------------------------------
# WORKING
@app.route('/receive', methods=['GET', 'POST'])
def receive():
    # Sends a request for payment
    
    def create_connection(db_file):
        """
        connection to the SQLite database
        """
        
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            print("Connected to wallet database")
        except Error as e:
            print(e)
        return conn

    def getPayments():
        #Returns all requests as a list of tuples
        # create a connection object
        dbPath = 'C:\Block_Wallet\wallet.db'
        conn = create_connection(dbPath)

        # create a cursor object
        c = conn.cursor()
    
        c.execute("SELECT * FROM payreq ORDER BY TimeStamp DESC")
    
        Req = c.fetchall()

        # Close the database connection
        c.close()
        
        # Convert list of tuples to a string
        # ready to display on website
        strReq = ""
        for x in Req:
            strReq = strReq + \
                     datetime.datetime.fromtimestamp(x[0]).strftime('%Y-%m-%d %H:%M:%S') + "\n" + \
                     str(x[1]) + "\n" + \
                     str(x[2]) + " Satoshi\n" + \
                     str(x[3]) + "\n"
            strReq = strReq + "\n"

        return strReq

     
    def saveNewPayment(Req):
        # Insert a requested Tx
        # Req is a tuple
        
        # create a connection object
        dbPath = 'C:\Block_Wallet\wallet.db'
        conn = create_connection(dbPath)

        # create a cursor object
        c = conn.cursor()
                     
        c.execute("INSERT INTO payreq(TimeStamp, Label, Amount, Message) VALUES(?, ?, ?, ?)", Req)
   
        # commit insert
        conn.commit()

        # Close the database connection
        conn.close()
        
        return
    
## Start of MAIN /receive--------------------------
    if request.method == 'POST':
        # This block is only entered when the form is submitted
        # if form has been submitted, clear form and add to history
        #Get UTC in Unix time (seconds since epoch)
        UTC = int(time.time())
        #time = UTC.strftime("%d-%b-%Y (%H:%M:%S)")
        
        label = request.form.get('label')
        amount = request.form.get('amount')
        unit = request.form.get('unit')
        message = request.form.get('msg')

        # Convert ammount to satoshi
        satoshi = toSatoshi(amount, unit)
        
        # Store new request for payment as a tuple
        newRequest = (UTC, label, satoshi, message)
        saveNewPayment(newRequest)
        return render_template('receive.html', title='Diphtherium Wallet', history=getPayments())
    
    #if no post received return empty form
    return render_template('receive.html', title='Diphtherium Wallet', history=getPayments())

# Transactions------------------------------------------------------------------------------------------
# DUMMY
@app.route('/trans')
def trans():
    # dummy code
    return render_template('trans.html', title='Diphtherium Wallet')


#NOT USED---------------------------------------------------------------------------------------------
@app.route('/submit', methods=['POST'])
def submit_textarea():
    """
    Endpoint to create a new transaction via our application.
    """
    post_content = request.form["content"]
    author = request.form["author"]

    post_object = {
        'author': author,
        'content': post_content,
    }

    # Submit a transaction
    new_tx_address = "{}/new_transaction".format(CONNECTED_NODE_ADDRESS)

    requests.post(new_tx_address,
                  json=post_object,
                  headers={'Content-type': 'application/json'})

    return redirect('/')



