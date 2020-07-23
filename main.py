# Game launch

from Game import Game

print("Welcome to the Battleship Game!\nLet's start!")
game = Game()
while True:
    print("There is your field: ")
    # Player's field
    print(game.field_with_ships())
    print(f"\nThis is {game.show_enemy_name()}'s field: ")
    # Enemy's field
    print(game.field_without_ships())
    # player choose coordinates to attack
    game.read_position()
