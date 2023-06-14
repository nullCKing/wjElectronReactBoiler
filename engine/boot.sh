@echo off
FOR /F "tokens=5" %%T IN ('netstat -a -n -o ^| findstr :1212') DO (
SET /A PID=%%T) &GOTO Kill
:Kill
IF DEFINED PID (
    ECHO Killing PID: %PID%
    taskkill /PID %PID% /F
) ELSE (
    ECHO No process found on port 1212
)