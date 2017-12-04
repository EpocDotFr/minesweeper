# Shell script to build the Minesweeper Mac OS executable.
# The resulting "minesweeper_mac.app" executable and "minesweeper_mac" script will be available in the "dist" directory.

pyinstaller \
    --clean --noconfirm --onefile --windowed \
    --log-level=WARN \
    --name="minesweeper_mac" \
    --icon="resources/images/icon.icns" \
    --add-data="resources:resources" \
    --osx-bundle-identifier="fr.epoc.python.games.minesweeper" \
    run.py