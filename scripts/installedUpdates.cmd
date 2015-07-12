@echo off

for /f "delims=" %%i in ('dir /S /B /A:-D %SystemRoot%\system32\CatRoot\*KB*.cat') do (
	for /f "tokens=1 delims= " %%a in ("%%~ti") do @echo %%a %%~ni
)
