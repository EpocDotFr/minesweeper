# Minesweeper

The [Minesweeper](https://en.wikipedia.org/wiki/Minesweeper_(video_game)) game, implemented in Python.

> TODO Screenshot

## Features

> TODO

## Prerequisites

Python 3. May eventually works with Python 2 (not tested).

## Installation

Clone this repo, and then the usual `pip install -r requirements.txt`.

## Usage

```
python run.py
```

### Controls

> TODO

## How it works

This game is built on top of [PyGame](http://www.pygame.org/hifi.html). I obviously can't explain how it
works here, so you'll have to jump yourself in the source code. Start with the entry point, `run.py`.

Beside the game itself, I use [PyInstaller](http://www.pyinstaller.org/) to generate the executables. It packs
up all the game and its assets in a single executable file so players just have to run it with nothing to install.
This task is performed by the `build_*` scripts to be run in the corresponding OS.

## Credits

  - Icon by [Oliver Scholtz](https://www.iconfinder.com/icons/23906/mines_icon) (freeware)

## End words

If you have questions or problems, you can [submit an issue](https://github.com/EpocDotFr/minesweeper/issues).

You can also submit pull requests. It's open-source man!