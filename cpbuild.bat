@echo off
setlocal

set DST_DIR=\\psbldfs\dfs\build\pt\pt856\856-106-R1\debug\WINX86

set DIR_LIST=^
psconfig.bat ^
ActiveX      ^
Apps         ^
appserv      ^
bin          ^
build        ^
class        ^
lib          ^
pgpsdk302    ^
secvault     ^
TUXEDO       ^
utility      ^
WEB          ^
src



for %%a in (%DIR_LIST%) do (
    echo %%a
)

if exist %DST_DIR% dir %DST_DIR%



:END
