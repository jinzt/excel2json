
:: 基于修改src code:https://github.com/zdhsoft/excel2json
:: pip install pyinstaller
:: pyinstaller -F excel2json.py

@echo off

:: delete all *.json
echo del all *.json
del /s *.json

:: covert config
excel2json.exe config.xlsx

pause
