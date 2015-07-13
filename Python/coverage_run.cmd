@echo off

:: setup.py install ( https://pypi.python.org/pypi/coverage )
:: pip install coverage 
:: easy_install coverage 

set CURRENT_DIR=%CD%
set PYTHONPATH=%CURRENT_DIR%

if [%1] == [] goto setDefCoverage
goto setCoverage

:setDefCoverage
set coverage=coverage
goto run
:setCoverage
set coverage=%1

:run

%coverage% erase
for %%x in ("%CURRENT_DIR%\*.py" "%CURRENT_DIR%\core\*.py" "%CURRENT_DIR%\db\*.py" "%CURRENT_DIR%\test\*.py") do %coverage% run --source=%CURRENT_DIR% --append %%x
%coverage% report --show-missing
