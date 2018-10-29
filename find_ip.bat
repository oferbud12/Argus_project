for /f "tokens=2 delims=:" %%a in ('ipconfig^|find "IPv4 Address"') do (
set ip=%%a
goto :BREAK
)

:BREAK
echo %ip: =% > scraper\host_ip.txt