@ECHO off
REM Batch script to build the Minesweeper Windows executable.
REM The resulting "minesweeper_windows.exe" executable will be available in the "dist" directory.

pyinstaller ^
    --clean --noconfirm --onefile --windowed ^
    --log-level=WARN ^
    --name="minesweeper_windows" ^
    --icon="resources/images/icon.ico" ^
    --add-data="resources;resources" ^
    run.py