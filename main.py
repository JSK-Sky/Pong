import pygame
from pygame.locals import *
from random import randint

pygame.init()
screen = pygame.display.set_mode((1200, 700), pygame.RESIZABLE)
x, y = screen.get_size()
clock = pygame.time.Clock()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

gameState = "Lobby"

running = True

p1Score = 0
p2Score = 0
p1y = round(y/2)-(round(y/5))/2
p2y = round(y/2)-(round(y/5))/2
ballx = x/2
bally = y/2
ballsize = x/50

speed1 = 5
speed2 = 8
direction = [0,0]
ball_wait_time = 0

lobbyButton = 0
last_change_time = 0
button_delay = 100

fontScore = pygame.font.Font("fonts/PressStart2P-Regular.ttf", 32)
fontTitle = pygame.font.Font("fonts/PressStart2P-Regular.ttf", 55)
fontButton = pygame.font.Font("fonts/PressStart2P-Regular.ttf", 30)
fontQuitInfo = pygame.font.Font("fonts/PressStart2P-Regular.ttf", 20)

def randomDirection():
    global i
    i = randint(speed1, speed2)
    r1 = randint(0, 1)
    r2 = randint(0, 1)
    
    direction[0] = i if r1 == 0 else -i
    direction[1] = i if r2 == 0 else -i
    
def afficher_texte(Surface, texte, font, x, y, couleur=(255, 255, 255)):
    texte_surface = font.render(texte, True, couleur)
    texte_rect = texte_surface.get_rect(center=(x, y))
    Surface.blit(texte_surface, texte_rect)


prev_x, prev_y = x, y

ballBounce = pygame.mixer.Sound("sounds/BallBounce.WAV")
ballBounce.set_volume(0.1)

backgroundMusic = pygame.mixer.Sound("musics/BackGroundMusic.MP3")
backgroundMusic.set_volume(0.05)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == VIDEORESIZE:
            ballx *= event.w / prev_x
            bally *= event.h / prev_y
            prev_x, prev_y = event.w, event.h
        if event.type == KEYDOWN:
            if gameState == "Lobby":
                if event.key == K_UP and lobbyButton != 0:
                    lobbyButton -= 1
                if event.key == K_DOWN and lobbyButton != 2:
                    lobbyButton += 1
                if event.key == K_RETURN:
                    if lobbyButton == 0:
                        ball_wait_time = pygame.time.get_ticks() + 1000
                        gameState = "Game"
                    elif lobbyButton == 1:
                        gameState = "Touches"
                    elif lobbyButton == 2:
                        running = False

            elif gameState == "Touches":
                if event.key == K_RETURN:
                    gameState = "Lobby"

    x, y = screen.get_size()
    
    if backgroundMusic.get_num_channels() == 0:
        backgroundMusic.play(-1)
    
    if gameState == "Lobby":        
        screen.fill(BLACK)
        
        afficher_texte(screen, "PONG", fontTitle, x/2, y/2-y/4, couleur=(255, 255, 255))
        
        if lobbyButton == 0:
            pygame.draw.rect(screen, WHITE, pygame.Rect(x/2 - 105, y/2 - 25, 210, 50))
            pygame.draw.rect(screen, BLACK, pygame.Rect(x/2 - 100, y/2 - 20, 200, 40))
        if lobbyButton == 1:
            pygame.draw.rect(screen, WHITE, pygame.Rect(x/2 - 165, y/2 + y/10 -30 -5, 320, 60))
            pygame.draw.rect(screen, BLACK, pygame.Rect(x/2 - 160, y/2 + y/10 -30, 310, 50))
        if lobbyButton == 2:
            pygame.draw.rect(screen, WHITE, pygame.Rect(x/2 - 105, y/2 + 2*(y/10) -30 -5, 200, 60))
            pygame.draw.rect(screen, BLACK, pygame.Rect(x/2 - 100, y/2 + 2*(y/10) -30, 190, 50))
        
        afficher_texte(screen, "Play", fontButton, x/2, y/2, couleur=(255, 255, 255))      
        afficher_texte(screen, "Touches", fontButton, x/2, y/2 + y/10, couleur=(255, 255, 255))      
        afficher_texte(screen, "Quit", fontButton, x/2, y/2 + 2*(y/10), couleur=(255, 255, 255))
        
        pygame.display.flip()

        clock.tick(60)
    
    elif gameState == "Touches":       
        screen.fill(BLACK)
        
        afficher_texte(screen, "Touches", fontTitle, x/2, y/2-y/4, couleur=(255, 255, 255))
        
        afficher_texte(screen, "Joueur 1 : Z - S", fontButton, x/2, y/2 - 40, couleur=(255, 255, 255))
        afficher_texte(screen, "Joueur 2 : UP - DOWN", fontButton, x/2, y/2, couleur=(255, 255, 255))
        
        afficher_texte(screen, "ENTER", fontQuitInfo, x-x/20, y-y/30, couleur=(255, 255, 255))
        
        pygame.display.flip()
        
        clock.tick(60)

    elif gameState == "Game":
        keys = pygame.key.get_pressed()
        if keys[K_z] and p1y > 5:
            p1y -= round(y/120)
        if keys[K_s] and p1y < y-round(y/5)-5:
            p1y += round(y/120)
            
        if keys[K_UP] and p2y > 5:
            p2y -= round(y/120)
        if keys[K_DOWN] and p2y < y-round(y/5)-5:
            p2y += round(y/120)
        
        p1x = 0 + 20
        p2x = x - 20 - round(x/35)
        
        if (ballx - ballsize <= p1x + round(x/35) and p1y <= bally <= p1y + round(y/5)):
            direction[0] = abs(direction[0])
            ballBounce.play()

        if (ballx + ballsize >= p2x and p2y <= bally <= p2y + round(y/5)):
            direction[0] = -abs(direction[0])
            ballBounce.play()

        if ballx <= ballsize:
            p2Score += 1
            ball_wait_time = pygame.time.get_ticks() + 2000
            ballx = x/2
            bally = y/2
            direction = [0, 0]
        if ballx >= x-ballsize:
            p1Score += 1
            ball_wait_time = pygame.time.get_ticks() + 2000
            ballx = x / 2
            bally = y / 2
            direction = [0, 0]
        if bally <= ballsize:
            direction[1] = -direction[1]
        if bally >= y-ballsize:
            direction[1] = -direction[1]
            
        if ball_wait_time and pygame.time.get_ticks() >= ball_wait_time:
            randomDirection()
            ball_wait_time = 0
        
        ballx += direction[0]
        bally += direction[1]

        screen.fill(BLACK)

        for i in range(0, y, 40):
            pygame.draw.rect(screen, WHITE, (x // 2 - 5, i, 10, 20))
            
        pygame.draw.rect(screen, WHITE, pygame.Rect(p1x, p1y, round(x/35), round(y/5)))
        pygame.draw.rect(screen, WHITE, pygame.Rect(p2x, p2y, round(x/35), round(y/5)))
        pygame.draw.circle(screen, WHITE, (ballx,bally), ballsize)
        
        afficher_texte(screen, f"{p1Score}", fontScore, x/2 - x/6, y/5, WHITE)
        afficher_texte(screen, f"{p2Score}", fontScore, x/2 + x/6, y/5, WHITE)
        
        pygame.display.flip()

        clock.tick(60)

pygame.quit()
