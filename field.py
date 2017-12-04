import settings
import random
import click


DIRECTIONS = (
    (0, -1), # Top
    (1, -1), # Top right
    (1, 0),  # Right
    (1, 1),  # Bottom right
    (0, 1),  # Bottom
    (-1, 1), # Bottom left
    (-1, 0), # Left
    (-1, -1) # Top left
)


class Area:
    nearby_mines_count = 0
    cleared = False # This area has been cleared, i.e do not contain any mine
    marked = False # This area has been marked as mined

    def __init__(self, has_mine):
        self.has_mine = has_mine

    @property
    def nearby_mines_count_color(self):
        """Return the color corresponding to the nearby mines count of this area."""
        return settings.NEARBY_MINES_COUNT_COLORS[self.nearby_mines_count] if self.nearby_mines_count in settings.NEARBY_MINES_COUNT_COLORS else None


class Field:
    field = []

    def __init__(self, width, height, mines):
        self.width = width
        self.height = height
        self.mines = mines
        self.areas = self.width * self.height

        if self.mines > self.areas:
            raise ValueError('Not enough space for {} mines'.format(self.mines))

        self._populate()
        self._compute_nearby_mines()

    def mark_area_as_mined(self, x, y):
        """Try to mark the area at the specified coordinates as mined."""
        if self.field[y][x].cleared:
            return False

        if self.field[y][x].marked:
            self.field[y][x].marked = False
        else:
            self.field[y][x].marked = True

        return True

    def mark_area_as_clear(self, x, y):
        """Try to mark the area at the specified coordinates as clear."""
        if self.field[y][x].cleared:
            return False

        self.field[y][x].cleared = True

        return True

    def print(self):
        """Print the current field state to stdout."""
        for y, row in enumerate(self.field):
            click.echo('{:>2} '.format(y), nl=False)

            for area in row:
                if area.has_mine:
                    out = 'X'
                    color = 'red'
                elif area.nearby_mines_count > 0:
                    out = str(area.nearby_mines_count)
                    color = 'cyan'
                else:
                    out = ' '
                    color = None

                click.secho(out, nl=False, fg=color)

            click.echo()

    def _generate_areas_with_mine(self):
        """Generate random mines position for the current field."""
        areas_with_mine = []

        for _ in range(0, self.mines):
            while True:
                random_area_number = random.randint(0, self.areas - 1)

                if random_area_number not in areas_with_mine:
                    areas_with_mine.append(random_area_number)

                    break

        return areas_with_mine

    def _populate(self):
        """Generate and place random mines for the current field."""
        areas_with_mine = self._generate_areas_with_mine()
        area_number = 0

        for y in range(0, self.height):
            row = []

            for x in range(0, self.width):
                row.append(Area(has_mine=area_number in areas_with_mine))

                area_number += 1

            self.field.append(row)

    def _compute_nearby_mines(self):
        """For each area that isn't mined, compute the surrounding mined areas."""
        for y, row in enumerate(self.field):
            for x, area in enumerate(row):
                if area.has_mine:
                    continue

                for direction in DIRECTIONS:
                    dir_x, dir_y = direction

                    nearby_x = x + dir_x
                    nearby_y = y + dir_y

                    if nearby_x < 0 or nearby_x > self.width - 1:
                        continue

                    if nearby_y < 0 or nearby_y > self.height - 1:
                        continue

                    if self.field[nearby_y][nearby_x].has_mine:
                        area.nearby_mines_count += 1
