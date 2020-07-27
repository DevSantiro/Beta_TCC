@echo off
set MODINSTALL9v24=C:\Repositorios_GIT\Beta-TCC\BetaTCC\media\Modeller9.24
set PYTHONPATH=C:\Repositorios_GIT\Beta-TCC\BetaTCC\media\Modeller9.24\modlib;
set LIB_ASGL=C:\Repositorios_GIT\Beta-TCC\BetaTCC\media\Modeller9.24\asgl
set BIN_ASGL=C:\Repositorios_GIT\Beta-TCC\BetaTCC\media\Modeller9.24\lib\x86_64-w64
set PATH=%MODINSTALL9v24%\lib\x86_64-w64;%PATH%
cd C:\Repositorios_GIT\Beta-TCC\BetaTCC\media

echo #########################################
echo ##### Modelagem Automatizada ############
echo #########################################

mod9.24 run.py
exit