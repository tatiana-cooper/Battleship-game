from Field import Field
from Player import Player


class Game:
    def __init__(self):
        """
        The class represented the BattleShips game process
        """
        player_1 = input('Player 1, Enter your name: ')
        player_2 = input('Player 2, Enter your name: ')
        self.__fields = [Field(), Field()]
        self.__players = [Player(player_1), Player(player_2)]
        self.__current_player = 0
        self.__next_player = 1

    def read_position(self):
        """
        The method performs the player's attack on enemy's field and checks winner
        :return: nothing
        """
        # player's chosen coordinates to attack
        pos = self.__players[self.__current_player].read_position()
        # enemy's field
        next_player_field = self.__fields[self.__next_player]
        # attack the enemy's field
        coord = next_player_field.field[pos[0]][pos[1]]
        coord.shoot_at()

        # if the enemy's field doesn't have alive ships — current player wins
        if next_player_field.alive == 0:
            print(f'☼ ☼ ☼ {self.__players[self.__current_player].show_name} is a winner! ☼ ☼ ☼')
            quit()

        # the next move of the enemy
        self.__current_player, self.__next_player = self.__next_player, self.__current_player

    def field_without_ships(self):
        """
        The enemy's field
        :return: field without ships
        """
        return self.__fields[self.__next_player].represent_field(with_ships=False)

    def field_with_ships(self):
        """
        The player's field
        :return: field with ships
        """
        return self.__fields[self.__current_player].represent_field(with_ships=True)

    def show_enemy_name(self):
        """
        :return: name of the current player's enemy
        """
        return self.__players[self.__current_player].show_name
