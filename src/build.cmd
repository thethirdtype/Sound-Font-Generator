@echo off

:: Set the target directory for executables
set ExecutablesDir=..\build

:PackageScript
if "%~1"=="" goto :BuildList
echo.
echo Builder started for %1. Next step, pyinstaller.
echo Press CTRL+C to abort or any key to continue...
pause > nul
echo.
pyinstaller %1 -F -i %2 -n %3
echo.
echo Pyinstaller finished for %1. Next step, cleanup.
echo Press CTRL+C to abort or any key to continue...
pause > nul
echo.
del %3.spec /F > nul
move dist\%3.exe "%ExecutablesDir%" > nul
rmdir /S /Q build > nul
rmdir /S /Q dist > nul
echo Finished for %1!
echo.
ping -n 2 127.0.0.1 > nul
goto :eof

:BuildList
call :PackageScript SoundFontForm.py sfg_icon.ico sfg
call :PackageScript SoundBenderForm.py sfg_icon.ico sfg_bender
