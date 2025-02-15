REM filepath: /d:/Python/CalendarScript/run_update_calendar.bat
@echo off
echo Starting the calendar update process...

echo Checking internet connection...
ping -n 1 www.google.com >nul 2>&1
if errorlevel 1 (
    echo No internet connection. Please check your connection and try again.
    pause
    exit /b
)

echo Internet connection is available.

echo Activating Python virtual environment...
call "D:\Python\CalendarScript\.venv\Scripts\activate.bat"

echo Running the update_calendar.py script...
python "D:\Python\CalendarScript\main.py"

REM Define file path and current time
set FILE_PATH="C:\Users\Armin\Downloads\icalexport.ics"
set /a TIME_LIMIT=10  REM Time limit to check (e.g., 10 seconds)

REM Get file's last modification time
for %%F in (%FILE_PATH%) do set FILE_MOD_TIME=%%~tF

REM Convert time to seconds
for /f "tokens=1,2,3 delims=/- " %%a in ("%FILE_MOD_TIME%") do (
    set /a "MOD_TIME=%%a*86400+%%b*3600+%%c*60"
)

REM Get current system time
for /f "tokens=1,2,3 delims=/- " %%a in ('echo %date%') do (
    set /a "CURRENT_TIME=%%a*86400+%%b*3600+%%c*60"
)

REM Calculate time difference
set /a TIME_DIFF=%CURRENT_TIME% - %MOD_TIME%

REM If time difference is less than LIMIT, show success message
if %TIME_DIFF% lss %TIME_LIMIT% (
    echo Calendar update process completed.
) else (
    echo No recent changes in the calendar file.
)

pause