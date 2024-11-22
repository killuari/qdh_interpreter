@echo off
for %%I in ("%~dp0") do set SCRIPT_DIR=%%~I
python "%SCRIPT_DIR%qdh.py" %*
