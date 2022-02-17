import time

import game
import gameParameters
import search
from drawGame import drawGameState
from gameParameters import NO_ROWS, NO_COLS
from  search import dfs,bfs,uni,astar,easyHeur,heur1,heur2
from drawGame import *
from  gameParameters import *
from main import pygame, screen, clock
import pygame_menu

from utils import loadImages


def set_difficulty(value, difficulty):
    gameParameters.DIFFICULTY=difficulty
    gameParameters.NO_COLS = (2 + min(max( gameParameters.DIFFICULTY , 1), 3))
    gameParameters.WIDTH = 100 * gameParameters.NO_COLS

def set_algorithm(value,algorithm):
    gameParameters.algoritm=algorithm

def set_heurName(value,heuristic):
    gameParameters.heuristicName=heuristic

def start_the_game():
    game.expandedNodes=0

    gs = game.createInitBoard()

    start = time.time()

    if(gameParameters.algoritm==astar):
        moves = gameParameters.algoritm(gs, gameParameters.heuristicName)
    else:
        moves = gameParameters.algoritm(gs)

    end = time.time()
    print("Time elapsed: ", end - start)

    print("mutari: ", len(moves))
    print("expandate: ", game.expandedNodes)


    gameScreen = pygame.display.set_mode((WIDTH, HEIGHT))
    i = 0
    loadImages()
    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
        drawGameState(gameScreen, gs)
        clock.tick(MAX_FPS)
        gs = game.makeMove(moves[i], gs)

        if(i< len(moves)-1):
            i += 1

        pygame.display.flip()


menu = pygame_menu.Menu('Guarini \'s puzzle', WIDTH, HEIGHT,
                        theme=pygame_menu.themes.THEME_BLUE)

menu.add.selector('Difficulty :', [('Easy', 1), ('Medium', 2), ('Difficult', 3)], onchange=set_difficulty)
menu.add.selector('Algorithm :', [('dfs', dfs), ('bfs', bfs), ('uni', uni),('aStar',astar)], onchange=set_algorithm)
menu.add.selector('Heuristic :', [('easy',easyHeur), ('heur1', heur1), ('heur2', heur2)], onchange=set_heurName)
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)
