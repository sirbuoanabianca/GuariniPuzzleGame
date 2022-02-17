import time

from  gameParameters import *
import GUI
import game
import search
from drawGame import *
from utils import *

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

def main():


    screen.fill(pygame.Color("white"))
    GUI.menu.mainloop(screen)


if __name__ == "__main__":
    main()
