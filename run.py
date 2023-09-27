# author: Mohamad Mahdi Reisi
# Date: 2023/8/16

# Description: This file is used to run the main.py file
# the reason for this file is that we want to run the main.py file from the root directory of the project
# so we can use the relative path to import the modules


import os 

file_path = os.path.abspath(__file__).split('run.py')[0]

# go to the file path address
os.chdir(file_path)

def run(map , genome1 , genome2 , genome3) :
    import src.blueprints.login as lg
    lg.player_id = 0
    import src.main as main
    import player0.data as p0d
    import player1.data as p1d
    import player2.data as p2d
    p0d.genomee = genome1
    p1d.genomee = genome2
    p2d.genomee = genome3
    main.main(map)

