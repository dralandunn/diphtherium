:: @ECHO OFF
ECHO Starting the Wallet server

:: Change CMD Window Title
TITLE Wallet Server

:: Install a Virtual Environment env
python -m venv env && ECHO Virtual Environment Created

:: Activate the environment
CALL env\Scripts\activate && ECHO Virtual Environment Activated

:: Install the required packages defined in requiments.txt
pip install -r requirements.txt && ECHO Packages Installed

:: Set sytem variable to tell Flask which app to run
set FLASK_APP=wallet.py && ECHO Flask app set

:: Run the Wallet server on actual IP (not loop back)
CALL flask run --port=5000 --host=0.0.0.0 && ECHO Wallet Server Started

:: Exit batch script
EXIT /B