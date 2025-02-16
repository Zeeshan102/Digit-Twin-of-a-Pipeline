@echo off
rem Navigate to the QGIS bin directory
cd /d "C:\Program Files\QGIS 3.34.1\bin"

rem Run QGIS process
call qgis_process-qgis.bat

rem Run Python script with QGIS, taking file paths as command-line arguments
python-qgis.bat %1 %2 %3

rem Display success message
echo Task completed successfully.

rem Pause to see the output before closing the command prompt
pause
