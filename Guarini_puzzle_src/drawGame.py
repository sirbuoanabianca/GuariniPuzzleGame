from utils import *
import pygame


def drawGameState(screen, gs):
    drawBoard(screen)
    drawKnigts(screen, gs)


def drawBoard(screen):
    colors = [pygame.Color("white"),
              pygame.Color("gray")]
    for r in range(gameParameters.NO_ROWS):
        for c in range(gameParameters.NO_COLS):
            color = colors[((r + c) % 2)]
            pygame.draw.rect(screen, color, pygame.Rect(c * gameParameters.SQ_SIZE, r * gameParameters.SQ_SIZE, gameParameters.SQ_SIZE, gameParameters.SQ_SIZE))


def drawKnigts(screen, board):
    for r in range(gameParameters.NO_ROWS):
        for c in range(gameParameters.NO_COLS):
            piece = board[r][c]
            if piece != '_':
                screen.blit(gameParameters.IMAGES[piece], pygame.Rect(c * gameParameters.SQ_SIZE, r * gameParameters.SQ_SIZE, gameParameters.SQ_SIZE, gameParameters.SQ_SIZE))
