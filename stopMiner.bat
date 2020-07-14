:: Cleans Up Virtual Environmentcd
@ECHO OFF
ECHO Exit Miner venv

:: Assumes venv is activated
:: create list of modules to remove
pip freeze > mod_list.txt

:: Uninstall modules and dependecies
pip uninstall -r mod_list.txt -y

deactivate

:: Remove venv folder (python installation)
:: /S deletes contents (of non-empty folder)
:: /Q supresses confirmation
rd /S /Q  env

:: Remove Python cache
rd /S /Q __pycache__
