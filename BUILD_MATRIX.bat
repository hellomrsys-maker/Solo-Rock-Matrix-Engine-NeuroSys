@echo off
echo =====================================================
echo  SOLO ROCK V4 MATRIX - STANDALONE COMPILER
echo =====================================================
echo Installing PyInstaller...
pip install pyinstaller
echo Generating Procedural Audio...
C:\Users\sysyo\AppData\Local\Python\pythoncore-3.14-64\python.exe generate_audio.py
echo Compiling realtime_boot.py into standalone Matrix.exe...
C:\Users\sysyo\AppData\Local\Python\pythoncore-3.14-64\python.exe -m PyInstaller --onefile --noconfirm --name MatrixV4 --add-data "wall_texture.bmp;." --add-data "gun_idle.bmp;." --add-data "gun_fire.bmp;." --add-data "assets/audio;assets/audio" realtime_boot.py
echo.
echo =====================================================
echo COMPILATION COMPLETE
echo The standalone engine is located at: dist\MatrixV4.exe
echo =====================================================
pause
