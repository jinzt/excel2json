
:: 基于修改src code:https://github.com/zdhsoft/excel2json
:: pip install pyinstaller
:: pyinstaller -F excel2json.py

@echo off

:: delete all *.json
echo del all *.json *.lua
del /s *.json
del /s *.lua

:: covert config
excel2json.exe config.xlsx

pause
