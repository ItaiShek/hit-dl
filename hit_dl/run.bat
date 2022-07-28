@echo off

echo	hit-dl Version 1.0.0
echo.

:USERNAME_LOOP
set /p user=Enter your username (or q to quit): 
if "%user%" == "" goto USERNAME_LOOP
if "%user%" == "q" goto END
if "%user%" == "Q" goto END
echo.

:PASSWORD_LOOP
set /p password=Enter your password (or q to quit): 
if "%password%" == "" goto PASSWORD_LOOP
if "%password%" == "q" goto END
if "%password%" == "Q" goto END
echo.

echo	You can enter multiple urls, when your'e done click enter without entering an input
set urls=
:URL_LOOP
set url=
set /p url=Enter a url (or q to quit): 
set urls=%urls% %url%
echo.
if "%url%" == "" goto RUN
if "%url%" == "q" goto END
if "%url%" == "Q" goto END
goto URL_LOOP

:RUN
hit-dl -u %user% -p %password% %urls%

pause > nul
:END