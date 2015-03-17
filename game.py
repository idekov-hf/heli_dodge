import pygame
import time
from random import randint, randrange

black = (0, 0, 0)
white = (255, 255, 255)

sunset = (253, 72, 47)

greenyellow = (184, 255, 0)
brightblue = (47, 228, 253)
orange = (255, 113, 0)
yellow = (255, 236, 0)
purple = (252, 67, 255)

colorChoices = [greenyellow, brightblue, orange, yellow, purple]

pygame.init()

surfaceWidth = 800
surfaceHeight = 500

imageHeight = 43
imageWidth = 100

surface = pygame.display.set_mode((surfaceWidth, surfaceHeight))
pygame.display.set_caption('Helicopter')
clock = pygame.time.Clock()

img1 = pygame.image.load('heli1.png')
img2 = pygame.image.load('heli2_2.png')


def score(count):
    font = pygame.font.Font('freesansbold.ttf', 20)
    text = font.render('Score: ' + str(count), True, white)
    surface.blit(text, [0, 0])


def blocks(x_block, y_block, block_width, block_height, gap, colorChoice):
    pygame.draw.rect(surface, colorChoice, [x_block, y_block, block_width, block_height])
    pygame.draw.rect(surface, colorChoice, [x_block, y_block + block_height + gap, block_width, block_height + (surfaceHeight - (y_block + block_height + gap))])


def replay_or_quit():
    for event in pygame.event.get([pygame.KEYDOWN, pygame.KEYUP, pygame.QUIT]):
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        elif event.type == pygame.KEYDOWN:
            continue

        return event.key

    return None


def makeTextObjs(text, font):
    textSurface = font.render(text, True, sunset)
    return textSurface, textSurface.get_rect()


def msgSurface(text):
    smallText = pygame.font.Font('freesansbold.ttf', 20)
    largeText = pygame.font.Font('freesansbold.ttf', 150)

    titleTextSurface, titleTextRect = makeTextObjs(text, largeText)
    titleTextRect.center = surfaceWidth / 2, surfaceHeight / 2
    surface.blit(titleTextSurface, titleTextRect)

    typTextSurface, typTextRect = makeTextObjs('Press any key to continue', smallText)
    typTextRect.center = surfaceWidth / 2, ((surfaceHeight / 2) + 100)
    surface.blit(typTextSurface, typTextRect)

    pygame.display.update()
    time.sleep(1)

    while replay_or_quit() == None:
        clock.tick()

    main()


def gameOver():
    msgSurface('Kaboom!')


def helicopter(x, y, image):
    surface.blit(image, (x, y))


def main():
    x = 150
    y = 200
    y_move = 0

    x_block = surfaceWidth
    y_block = 0

    block_width = 75
    block_height = randint(0, surfaceHeight - 200)
    gap = imageHeight * 3
    block_move = 3

    current_score = 0

    blockColor = colorChoices[randrange(0, len(colorChoices))]

    rotor = 0

    game_over = False

    while not game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    y_move = -5
                if event.key == pygame.K_d:
                    y_move = 0
                if event.key == pygame.K_q:
                    game_over = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    y_move = 5
                if event.key == pygame.K_q:
                    game_over = True
                    pygame.quit()
                    quit()

        y += y_move

        surface.fill(black)

        if rotor <= 5:
            helicopter(x, y, img1)
            rotor += 1
        elif 5 < rotor <= 10:
            helicopter(x, y, img2)
            rotor += 1
            if rotor == 10:
                rotor = 0


        blocks(x_block, y_block, block_width, block_height, gap, blockColor)
        score(current_score)
        x_block -= block_move

        if y > surfaceHeight - 40 or y < 0:
            gameOver()

        if x_block < (-1 * block_width):
            x_block = surfaceWidth
            block_height = randint(0, surfaceHeight - imageHeight)
            blockColor = colorChoices[randrange(0, len(colorChoices))]
            current_score += 1

        if x + imageWidth > x_block:
            if x < x_block + block_width:
                # print 'possibly within the boundaries of x'
                if y < block_height:
                    # print 'y crossover UPPER!'
                    if x - imageWidth < block_width + x_block:
                        # print 'game over hit upper'
                        gameOver()

        if x + imageWidth > x_block:
            # print 'x crossover'
            if y + imageHeight > block_height + gap:
                # print 'y crossover lower'
                if x < block_width + x_block:
                    # print 'game over lower'
                    gameOver()

        if current_score == 3:
            block_move = 5
            gap = imageHeight * 2.6
        if current_score == 6:
            block_move = 6
        if current_score == 9:
            block_move = 7

        pygame.display.update()
        clock.tick(60)


main()
pygame.quit()
quit()