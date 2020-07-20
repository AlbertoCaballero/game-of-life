import pygame
import numpy as np
import time

# Init and define window
pygame.init()
pygame.display.set_caption('Game of Life')
widht, height = 700, 700
screen = pygame.display.set_mode((height, widht))

# Define background color
bg = 25, 25, 25
screen.fill(bg)

# Number of cells
nxC, nyC = 50, 50

# Cell dimentions
dimCW = widht / nxC
dimCH = height / nyC

# Cells state. Alive = 1, Dead = 0
state = np.zeros((nxC, nyC))

# Ask for the initial state of the game
print("\nInitial state file: ")
inputstate = input()

if inputstate == '':
    state == np.genfromtxt('default.csv')
else:
    state = np.genfromtxt(inputstate)

# In execution
executing = False

# Main loop
while True:

    # Copy current state to new state
    newState = np.copy(state)

    # Clear screen
    screen.fill(bg)

    # Wait some time
    time.sleep(0.1)

    # Get keyboard and mouse input
    events = pygame.event.get()

    # Event process
    for event in events:
        # Keyboard event
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Pause executing state
                executing = not executing
                print("Execution toggle")
            if event.key == pygame.K_RETURN:
                # Print current state to file
                np.savetxt("state.csv", state)
                print("Copied to file")

    # Mouse event
    clicks = pygame.mouse.get_pressed()

    if sum(clicks) > 0:
        posX, posY = pygame.mouse.get_pos()
        celX, celY = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH))
        newState[celX, celY] = not clicks[2]

    for y in range(0, nxC):
        for x in range(0, nyC):
            if not executing:
                # Calculate near alive neighbors
                neighbors = state[(x - 1) % nxC, (y - 1) % nyC] + \
                            state[(x)     % nxC, (y - 1) % nyC] + \
                            state[(x + 1) % nxC, (y - 1) % nyC] + \
                            state[(x - 1) % nxC, (y)     % nyC] + \
                            state[(x + 1) % nxC, (y)     % nyC] + \
                            state[(x - 1) % nxC, (y + 1) % nyC] + \
                            state[(x)     % nxC, (y + 1) % nyC] + \
                            state[(x + 1) % nxC, (y + 1) % nyC]

                # Rule 1: Dead cell with exactly 3 alive neighbors, relives
                if state[x, y] == 0 and neighbors == 3:
                    newState[x, y] = 1

                # Rule 2: Living cell with less of 2 or more than 3 alive neighbors, dies
                if state[x, y] == 1 and (neighbors < 2 or neighbors > 3):
                    newState[x, y] = 0


            # Define polygon shape
            poly =  [((x)  * dimCW, y     * dimCH),
                    ((x+1) * dimCW, y     * dimCH),
                    ((x+1) * dimCW, (y+1) * dimCH),
                    ((x)   * dimCW, (y+1) * dimCH)]


            if newState[x, y] == 0:
                pygame.draw.polygon(screen, (128, 128, 128), poly, 1)
            else:
                pygame.draw.polygon(screen, (3, 252, 157), poly, 0)

    # Update game state
    state = np.copy(newState)

    # Display to screen
    pygame.display.flip()
