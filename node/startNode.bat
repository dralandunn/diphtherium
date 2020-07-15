@ECHO OFF
ECHO Starting the blockchain node server
TITLE Node Server

:: Install a Virtual Environment env
python -m venv env && ECHO Virtual Environment Created

:: Activate the environment
CALL env\Scripts\activate && ECHO Virtual Environment Activated

:: Install the required packages defined in requirements.txt:
pip install -r requirements.txt && ECHO Packages Installed

:: Set sytem variable to tell Flask which app to run:
set FLASK_APP=node_server.py && ECHO Flask app set

:: Run the Node server on actual IP (not loop back)
ECHO Starting Node Server
flask run --port=8000 --host=0.0.0.0