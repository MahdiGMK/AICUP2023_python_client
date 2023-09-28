# author: Mohamad Mahdi Reisi

# this is the main file of the game that will run the game
# this file reads the map file and creates a game object and initializes it
# then make a server
# and add different APIs from blueprints to the server
# it also has a function to kill the server

from src.components.game import Game
import src.tools.read_config as read_config
from src.turn_controllers.change_turn import change_turn
import os
import argparse

def main(map) :
    # define argument parser
    parser = argparse.ArgumentParser(description='choose map to play on')
    parser.add_argument('-m', '--map', type=str, help='choose map to play on')
    args = parser.parse_args()

    # read map file 
    main_game = Game()

    # ask player to choose map from the list of maps
    maps = os.listdir('maps')

    ## get the selected map from the player
    # selected_map = str(maps.index(args.map)) if args.map != None else "None"

    # while selected_map.isdigit() == False or int(selected_map) >= len(maps) or int(selected_map) < 0:
    #     ## show the list of maps from the maps folder
    #     print("Choose a map from the list of maps:")
    #     for i, map in enumerate(maps):
    #         print(i,'-', map)
    #     selected_map = input("Enter the number of the map you want to choose: ")

    ## read the selected map
    main_game.read_map('maps/'+map)

    main_game.config = read_config.read_config()

    # set the debug variable to True or False to see the debug messages and generate debug logs 
    debug = main_game.config['debug']

    main_game.debug = debug


    # Todo: Build Clients
    from src.components.client_game import ClientGame
    from player0.initialize import initializer as initializer_p0
    from player1.initialize import initializer as initializer_p1
    from player2.initialize import initializer as initializer_p2

    client_game = ClientGame(main_game)

    initializer_p0(client_game)
    initializer_p1(client_game)
    initializer_p2(client_game)

    # Todo: run the server

    if main_game.game_started:
        change_turn(main_game, client_game)
    return main_game.log['score']
