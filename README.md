# Minesweeper

The [Minesweeper](https://en.wikipedia.org/wiki/Minesweeper_(video_game)) game, implemented in Python.

<p align="center">
  <img src="https://raw.githubusercontent.com/EpocDotFr/minesweeper/master/screenshot.png">
</p>

## Features

  - All the Minesweeper rules
  - State of the art graphics
  - Automatic game saving when quitting. If there's a saved game it is automatically loaded, too
  - Stats
  - Sound effects!

## Prerequisites

Python 3. May eventually works with Python 2 (not tested).

## Installation

Clone this repo, and then the usual `pip install -r requirements.txt`.

## Usage

```
python run.py
```

### Controls

  - <kbd>ESC</kbd> closes the game
  - <kbd>F1</kbd> starts a new game
  - <kbd>F2</kbd> displays stats
  - <kbd>LMB</kbd> clears an area
  - <kbd>RMB</kbd> place a mine marker on an area

## How it works

This game is built on top of [PyGame](http://www.pygame.org/hifi.html). I obviously can't explain how it
works here, so you'll have to jump yourself in the source code. Start with the entry point, `run.py`.

Beside the game itself, I use [PyInstaller](http://www.pyinstaller.org/) to generate the executables. It packs
up all the game and its assets in a single executable file so players just have to run it with nothing to install.
This task is performed by the `build_*` scripts to be run in the corresponding OS.

## Credits

  - Icon by [Oliver Scholtz](https://www.iconfinder.com/icons/23906/mines_icon) (freeware)
  - Font by [Typodermic Fonts Inc](http://www.dafont.com/coolvetica.font) (freeware)
  - Graphics by [Kenney](https://kenney.nl/assets/topdown-tanks-redux) (CC0 1.0 Universal)
  - Sound effects by [Freesfx.co.uk](http://www.freesfx.co.uk/) (© Freesfx.co.uk) and [Kenney](https://kenney.nl/assets/voiceover-pack) (CC0 1.0 Universal)

## End words

If you have questions or problems, you can [submit an issue](https://github.com/EpocDotFr/minesweeper/issues).

You can also submit pull requests. It's open-source man!