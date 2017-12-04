# Shell script to build the Minesweeper Linux executable.
# The resulting "minesweeper_linux" script will be available in the "dist" directory.

pyinstaller \
    --clean --noconfirm --onefile \
    --log-level=WARN \
    --name="minesweeper_linux" \
    --add-data="resources:resources" \
    run.py