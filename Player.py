from string import digits


class Player:

    def __init__(self, name):
        """
        Represented the player of the BattleShips game
        :param name: name of the player
        """
        self.__name = name

    @property
    def show_name(self):
        """
        This method returns the attribute __name
        :return: __name
        """
        return self.__name

    def read_position(self):
        """
        The method reads coordinates entered by player
        :return: coordinates
        """
        letters = " ABCDEFGHIJ"  # needed to convert letters to int

        while True:

            coordinates = input(
                f'Player {self.__name} choose your coordinates from 1 to 10 and from A to J using the space: ').split()
            if coordinates[0] in digits and coordinates[1] in letters.strip():
                return int(coordinates[0]), letters.index(coordinates[1])
