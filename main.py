import sys, pygame, random, pandas as pd
from ship import Ship
from asteroid import Asteroid
import matplotlib.pyplot as plt
import numpy as np
from pygame.locals import *

pygame.init()
screen_info = pygame.display.Info()

size = (width, height) = (int(screen_info.current_w * 0.5), int(screen_info.current_h * 0.5))

screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
color = (20, 10, 40)
screen.fill(color)

#read and store game data
df = pd.read_csv('game_info.csv')

#set up game vars
asteroids = pygame.sprite.Group()
numLevels = df['LevelNum'].max()
level = df['LevelNum'].min()
levelData = df.iloc[level]
asteroidCount = levelData['AsteroidCount']
player = Ship((levelData['PlayerX'], levelData['PlayerY']))
tries = 0
totalTries = []

def init():
    global asteroidCount, asteroids, levelData, tries
    levelData = df.iloc[level]
    player.reset((levelData['PlayerX'], levelData['PlayerY']))
    asteroids.empty()s
    asteroidCount = levelData['AsteroidCount']
    for i in range(asteroidCount):
        asteroids.add(Asteroid((random.randint(50, width - 50), random.randint(50, height - 50)), random.randint(15,60)))
    tries = 1

def win():
    font = pygame.font.SysFont(None, 70)
    text = font.render('You Won!', True, (0,255,0))
    text_rect = text.get_rect()
    text_rect.center = (width/2, height/2)
    #create bar graph
    index = np.arange(len(totalTries))
    plt.bar(index, totalTries)
    plt.xlabel('Level #', fontsize=15)
    plt.ylabel('# of Tries', fontsize=15)
    plt.xticks(index, totalTries, fontsize=20, rotation=5)
    plt.title('Tries per Level')
    plt.show()

    while True:
        screen.fill(color)
        screen.blit(text, text_rect)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()

def main():
    global level, tries, totalTries
    init()
    while level <= numLevels:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_d:
                    player.speed[0] = 5
                if event.key == K_a:
                    player.speed[0] = -5
                if event.key == K_w:
                    player.speed[1] = -5
                if event.key == K_s:
                    player.speed[1] = 5
            if event.type == KEYUP:
                if event.key == K_d:
                    player.speed[0] = 0
                if event.key == K_a:
                    player.speed[0] = 0
                if event.key == K_w:
                    player.speed[1] = 0
                if event.key == K_s:
                    player.speed[1] = 0
        screen.fill(color)
        player.update()
        asteroids.update()
        gets_hit = pygame.sprite.spritecollide(player, asteroids, False)
        asteroids.draw(screen)
        screen.blit(player.image, player.rect)
        pygame.display.flip()

        if player.checkReset(width):
            totalTries.append(tries)
            if level == numLevels:
                break
            else:
                level += 1
                init()
        elif gets_hit:
            player.reset((levelData['PlayerX'], levelData['PlayerY']))
            tries += 1

    win()

if __name__ == '__main__':
    main()