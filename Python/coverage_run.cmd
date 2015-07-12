@echo off

:: setup.py install ( https://pypi.python.org/pypi/coverage )
:: pip install coverage 
:: easy_install coverage 

set CURRENT_DIR=%CD%
set PYTHONPATH=%CURRENT_DIR%

coverage erase
for %%x in ("%CURRENT_DIR%\*.py" "%CURRENT_DIR%\core\*.py" "%CURRENT_DIR%\db\*.py" "%CURRENT_DIR%\test\*.py") do coverage run -a %%x
coverage report -m
