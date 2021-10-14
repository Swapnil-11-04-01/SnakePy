import pygame
import random
import os



pygame.init()
pygame.mixer.init()



# Colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
green = (0, 255, 0)
yellow = (255, 255, 0)



# Creating window
screen_width = 900
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width, screen_height))



# Game Title
pygame.display.set_caption("Snakes by MASTERVERSE")
pygame.display.update()

font = pygame.font.SysFont('Sans', 40)




def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])




def plot_snake(gameWindow, color, snk_list, snake_size):
    for x, y in snk_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])



# Welcome Page
def welcome():


    pygame.mixer.Channel(0).play(pygame.mixer.Sound('bgsound.wav'))
    exit_game = False



    while not exit_game:

        bgimg = pygame.image.load("bg1.jpg")
        bgimg = pygame.transform.scale(bgimg, (screen_width, screen_height)).convert_alpha()
        gameWindow.blit(bgimg, (0, 0))


        text_screen("Press 'Space Bar' To Play", white, 260, 430)


        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                exit_game = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    gameloop()


        pygame.display.update()
        #clock.tick(60)




# Game loop
def gameloop():


    # Game specific variables
    exit_game = False
    game_over = False
    snake_x = 50
    snake_y = 50
    velocity_x = 0
    velocity_y = 0
    food_x = random.randint(20, screen_width / 2)
    food_y = random.randint(20, screen_height / 2)
    score = 0
    velocity_init = 1
    snake_size = 20
    fps = 120
    snk_list = []
    snk_length = 1



    pygame.mixer.Channel(0).stop()



    # Check if hiscore file exists
    if not os.path.exists("hiscore.txt"):
        with open("hiscore.txt", "w") as f:
            f.write("0")

    with open("hiscore.txt", "r") as f:
        hiscore = f.read()



    # Game Background
    bgimg = pygame.image.load("bg2.jpg")
    bgimg = pygame.transform.scale(bgimg, (screen_width, screen_height)).convert_alpha()
    gameWindow.blit(bgimg, (0, 0))



    while not exit_game:

        if game_over:
            with open("hiscore.txt", "w") as f:
                f.write(str(hiscore))


            # Main Screen Background Image                                                          
            bgimg = pygame.image.load("GameOver.png")
            bgimg = pygame.transform.scale(bgimg, (screen_width, screen_height)).convert_alpha()
            gameWindow.blit(bgimg, (0, 0))


            # gameWindow.fill(black)
            if int(hiscore) > score:
                text_screen("Press 'Enter' To Continue", white, 275, 500)

            else:
                text_screen(f"NEW HIGHSCORE : {hiscore}", green, 280, 75)
                text_screen("Press 'Enter' To Continue", white, 275, 500)


            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        exit_game = True
                        welcome()


        else:
            for event in pygame.event.get():


                if event.type == pygame.QUIT:
                    exit_game = True


                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = velocity_init
                        velocity_y = 0

                    if event.key == pygame.K_DOWN:
                        velocity_y = velocity_init
                        velocity_x = 0

                    if event.key == pygame.K_LEFT:
                        velocity_x = -velocity_init
                        velocity_y = 0

                    if event.key == pygame.K_UP:
                        velocity_y = -velocity_init
                        velocity_x = 0

                    if event.key == pygame.K_s:
                        score += 10

                    if event.key == pygame.K_v:
                        velocity_init -= 0.5


            snake_x += velocity_x
            snake_y += velocity_y


            if abs(snake_x - food_x) < 15 and abs(snake_y - food_y) < 15:
                score += 10
                food_x = random.randint(20, screen_width)
                food_y = random.randint(20, screen_height)
                snk_length += 5
                velocity_init += 0.3
                pygame.mixer.Channel(1).play(pygame.mixer.Sound('score.wav'))


                if score > int(hiscore):
                    hiscore = score


            gameWindow.fill(white)
            gameWindow.blit(bgimg, (0, 0))
            text_screen(f"Score: {score}  /  Hiscore: {hiscore}", white, 250, 5)
            pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size])


            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)


            if len(snk_list) > snk_length:
                del snk_list[0]

            if snake_x > 900:
                snake_x = 0
            if snake_x < 0:
                snake_x = 900
            if snake_y > 600:
                snake_y = 0
            if snake_y < 0:
                snake_y = 600


            if head in snk_list[:-1]:
                game_over = True
                pygame.mixer.stop()

                if int(hiscore) > score:
                    pygame.mixer.music.load('GameOverBG.wav')
                    pygame.mixer.music.play()

                else:
                    pygame.mixer.music.load('highscore.wav')
                    pygame.mixer.music.play()


            plot_snake(gameWindow, yellow, snk_list, snake_size)


        pygame.display.update()
        #clock.tick(fps)



    pygame.quit()
    quit()


welcome()