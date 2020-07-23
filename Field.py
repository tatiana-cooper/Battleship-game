from itertools import product
import random
from Ship import Ship
from Cell import Cell


class Field:

    def __init__(self):
        """
        Initialize a new field.
        """
        self.field = self.generate_field()
        self.__alive = 20  # not damaged ship-cells

    @property
    def alive(self):
        return self.__alive

    def shoot_at(self):
        """
        TODO
        :return:
        """
        self.__alive -= 1

    def represent_field(self, with_ships=True):
        """
        View of field.
        (bool) -> (str)
        :param with_ships: bool parameter, which shows if we print enemy's field with unseen ships or current player's
        field
        :return: view of field
        """
        str_field = " A̲ B̲ C̲ D̲ E̲ F̲ G̲ H̲ I̲ J̲\n"
        for i in range(0, 12):
            for j in range(0, 12):
                field_cell = self.field[i][j]
                if (i, j) in [(0, j), (11, j)]:  # border
                    str_field += '——'
                elif (i, j) == (i, 11):  # the right border with digit
                    str_field += f'|{i}'
                elif (i, j) == (i, 0):  # to avoid numerical problems with starting count from 0
                    str_field += ''
                elif isinstance(field_cell, Cell):
                    str_field += field_cell.view()
                elif isinstance(field_cell, Ship):
                    if with_ships:
                        str_field += field_cell.view()
                    else:
                        if field_cell.is_damaged:
                            str_field += field_cell.view()
                        else:
                            str_field += '| '

            str_field += '\n'
        return str_field

    def generate_field(self):
        """
        The method generates Battleship field 10x10
        (tpl(int, int)) -> (str)
        :return: the field
        """
        field_size = (12, 12)  # size of the field (12x12 including the border)
        # field of the Cell objects
        self.field = [[Cell() for _ in range(field_size[0])] for _ in range(field_size[1])]

        # types of needed ships_types for the game, key — the size of the ship, value — the number of ships_types
        ships_types = {4: 1, 3: 2, 2: 3, 1: 4}
        x = range(1, 11)  # counting from 1 because of the border
        y = range(1, 11)
        all_coords = [(x, y) for x, y in product(x, y)]  # all coordinates of the field

        for key, value in ships_types.items():
            for _ in range(value):
                ship_coordinates = self.ship_spots_decider(all_coords, key)

                for selected_coord in ship_coordinates:
                    ship = Ship()
                    self.field[selected_coord[0]][selected_coord[1]] = ship

                    # remove already used coordinates to avoid the same coordinate selection
                    all_coords.remove((selected_coord[0], selected_coord[1]))

                # delete all the free cells coordinates near the ship to avoid
                # placing ships one by one without space between
                for x_1, y_1 in ship_coordinates:
                    lst = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
                    for x_2, y_2 in lst:
                        if (x_1 + x_2, y_1 + y_2) in all_coords and isinstance(self.field[x_1 + x_2][y_1 + y_2], Cell):
                            all_coords.remove((x_1 + x_2, y_1 + y_2))

        return self.field

    def ship_spots_decider(self, all_coords, ship_size):
        """
        The method generates random coordinates for building the ship
        (list(tuple(int, int)), int) -> (list(tuples))
        :param all_coords: all free coordinates of the field
        :param ship_size: the size of the ship
        :return: list of the coordinates
        """
        direction = random.choice(['v', 'h'])  # v - vertical, h - horizontal
        selected_coord = random.choice(all_coords)
        ship_coordinates = self.check_ship_place(selected_coord, all_coords, direction, ship_size)

        # if all of the coordinates are valid
        if ship_coordinates is not None:
            ship_coordinates.append(selected_coord)
            return ship_coordinates

        else:
            # recursion until valid coordinates are selected
            return self.ship_spots_decider(all_coords, ship_size)

    def check_ship_place(self, selected_coord, valid_coords, direction, ship_size, count=1):
        """
        (tuple(int, int), [tuple(int, int)..], str, int, int) -> boolean
        The method checks if the coordinates are valid for spotting ship
        :param selected_coord: chosen coordinates by random
        :param valid_coords: all free coordinates of the field
        :param direction: v - vertical, h - horizontal
        :param ship_size: the size of the ship
        :param count: counter for recursion exit. If count == 3 — end of the recursion.
                Recursion calls with the opposite parameter of direction (v or h)
        :return: bool (True if coordinates are valid, False vice versa)
        """

        ship_coordinates = []

        if selected_coord not in valid_coords:
            return None

        if count == 3:  # if all of the directions are tested and not suitable for spotting ship (v and h)
            return None

        if direction == 'h':

            # choose the direction of the ship — right or left
            if selected_coord[1] - ship_size < 0:  # the left direction not valid, move in right direction

                # from 1 because we have had already selected the first coordinate
                for part_ship in range(1, ship_size):

                    # coordinates of the next part of the ship
                    coord = (selected_coord[0], selected_coord[1] + part_ship)

                    # if coordinates of the next part of the ship are in the list of valid coordinates of the field
                    if coord in valid_coords:
                        ship_coordinates.append(coord)

                    else:
                        # recursion call with opposite direction
                        count += 1
                        return self.check_ship_place(selected_coord, valid_coords, 'v', ship_size, count)

            else:  # the right direction not valid, move in left direction
                for part_ship in range(1, ship_size):
                    coord = (selected_coord[0], selected_coord[1] - part_ship)
                    if coord in valid_coords:
                        ship_coordinates.append(coord)

                    else:
                        count += 1
                        return self.check_ship_place(selected_coord, valid_coords, 'v', ship_size, count)

        elif direction == 'v':
            # choose the direction of the ship — top or down
            if selected_coord[0] - ship_size < 0:  # the top direction not valid, move in down direction

                for part_ship in range(1, ship_size):
                    coord = (selected_coord[0] + part_ship, selected_coord[1])
                    if coord in valid_coords:
                        ship_coordinates.append(coord)

                    else:
                        count += 1
                        return self.check_ship_place(selected_coord, valid_coords, 'h', ship_size, count)

            else:  # the down direction not valid, move in top direction
                for part_ship in range(1, ship_size):
                    coord = (selected_coord[0] - part_ship, selected_coord[1])
                    if coord in valid_coords:
                        ship_coordinates.append(coord)

                    else:
                        count += 1
                        return self.check_ship_place(selected_coord, valid_coords, 'h', ship_size, count)

        # + 1 from 1 because we have had already selected the first coordinates
        if len(ship_coordinates) + 1 == ship_size:
            return ship_coordinates

        else:
            return None
