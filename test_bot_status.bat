@echo off
echo Testing bot status...
curl "https://api.telegram.org/bot8634281755:AAEdhfrDSO1-amh0ws6OrKTsIp_i3R9C2aQ/getUpdates?timeout=1"
echo.
echo.
echo If you see "ok":true with no errors, the bot is ready for fresh deployment.
pause
