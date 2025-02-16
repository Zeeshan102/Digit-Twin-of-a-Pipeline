@echo off
rem Navigate to the OSGeo4W bin directory
cd /d "C:\OSGeo4W\bin"

rem Run the o4w_env.bat file
call o4w_env.bat

rem  execute python3.bat
call qgis_process-qgis-ltr.bat

python-qgis-ltr.bat  %1 %2

rem Display success message
echo Task completed successfully.

rem Pause to see the output before closing the command prompt
pause