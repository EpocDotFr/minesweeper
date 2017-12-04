import sys
import os

# ----------------------------------------------------------------------
# Editable settings

FPS = 30

AREAS_SIDE_SIZE = 25

WIDTH = 30
HEIGHT = 16
MINES = 99

GRID_SPACING = 1
GRID_COLOR = (195, 195, 195)

NEARBY_MINES_COUNT_COLORS = {
    1: (0, 0, 255),
    2: (0, 123, 0),
    3: (255, 0, 0),
    4: (0, 0, 123),
    5: (123, 0, 0),
    6: (0, 123, 123),
    7: (0, 0, 0),
    9: (123, 123, 123)
}

MUSIC_VOLUME = 0.2
SOUNDS_VOLUME = 0.3

# ----------------------------------------------------------------------
# Game constants - do not edit anything after this line

# When frozen by PyInstaller, the path to the resources is different
RESOURCES_ROOT = os.path.join(sys._MEIPASS, 'resources') if getattr(sys, 'frozen', False) else 'resources'

WINDOW_SIZE = (
    WIDTH * AREAS_SIDE_SIZE + (WIDTH - 1) * GRID_SPACING,
    HEIGHT * AREAS_SIDE_SIZE + (HEIGHT - 1) * GRID_SPACING
)
