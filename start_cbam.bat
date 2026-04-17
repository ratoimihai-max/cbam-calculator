@echo off
cd /d "%~dp0"
echo Pornesc aplicatia Calculator CBAM...
echo.
echo Pe acest calculator: http://localhost:8000
echo Pentru colegi: folositi adresa IP a acestui calculator, de forma http://IP-CALCULATOR:8000
echo.
python web_app.py
pause
