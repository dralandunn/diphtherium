# My Blockchain Node App

Runs the app: node_server.py

## Instructions to run

## Install a Virtual Environment env
C:\Block_Node>python -m venv env

## Activate the environment
C:\Block_Node>env\Scripts\activate

##Install the required packages defined in requirements.txt:
C:\Block_Node>pip install -r requirements.txt

##Set sytem variable to tell Flask which app to run:
C:\Block_Node>set FLASK_APP=node_server.py

## Run the server
C:\Block_Node>flask run --port=8000


One instance of node_sever.py is now up and running at port 8000.

