import pygame
import random

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

full_height = 80
duck_height = 40

player_height = full_height
player_width = 40

player_x = 400
player_y = 400

jump_target = 360  # Target y-coordinate for jumping
jump_speed = 0  # Initial jump speed
jump_acceleration = -0.5  # Acceleration for the jump
gravity = 0.5  # Gravity applied to the player

obstacle_width = 40
obstacle_height = 40
obstacle_x = 1240
obstacle_y = 440
obstacle_speed = 10  # Speed at which the obstacle moves to the left

on_ground = True
ascending = False  # Flag to track if the player is ascending or descending

game_over = False

score = 0

game_font = pygame.font.Font(None, 36)  # Font for displaying the score

add_score = True

def spawn_obstacle():
    global obstacle_x, obstacle_y
    obstacle_x = 1240
    obstacle_y = random.choice([380, 440])

spawn_obstacle()

def perform_action(action):
    global on_ground, ascending, jump_speed, player_height, player_y

    if action == 1 and on_ground:
        on_ground = False
        ascending = True
        jump_speed = -10
    elif action == 2 and on_ground:
        player_height = duck_height
        player_y = 440

def update_game_state():
    global on_ground, player_y, jump_speed, ascending, player_height, game_over

    if not on_ground:
        if ascending:
            player_y += jump_speed
            jump_speed += jump_acceleration

            if player_y <= jump_target:
                ascending = False

        else:
            player_y += jump_speed
            jump_speed += gravity

        if player_y >= 400 and not on_ground:
            player_y = 400
            on_ground = True
            jump_speed = 0

def check_collision():
    global game_over

    player = pygame.Rect(player_x, player_y, player_width, player_height)
    obstacle = pygame.Rect(obstacle_x, obstacle_y, obstacle_width, obstacle_height)

    if player.colliderect(obstacle):
        game_over = True

def update_score():
    global score, add_score

    if obstacle_x < player_x and add_score:
        score += 50
        add_score = False

def reset_game():
    global on_ground, ascending, jump_speed, player_height, player_y, game_over, score, add_score

    on_ground = True
    ascending = False
    jump_speed = 0
    player_height = full_height
    player_y = 400
    game_over = False
    score = 0
    add_score = True
    spawn_obstacle()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and game_over:
            if replay_button.collidepoint(event.pos):
                reset_game()

    screen.fill("#f0efef")

    if not game_over:
        action = 0  # Placeholder for the Q-learning agent's action
        perform_action(action)
        update_game_state()
        check_collision()
        update_score()

        player = pygame.Rect(player_x, player_y, player_width, player_height)
        obstacle = pygame.Rect(obstacle_x, obstacle_y, obstacle_width, obstacle_height)

        pygame.draw.rect(screen, "black", player)
        pygame.draw.rect(screen, "black", obstacle)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and on_ground:
            perform_action(1)
        if keys[pygame.K_s] and on_ground:
            perform_action(2)
        elif on_ground:
            player_y = 400
            player_height = full_height

        obstacle_x -= obstacle_speed

        if obstacle_x <= 0:
            add_score = True
            spawn_obstacle()

    score_text = game_font.render("Score: " + str(score), True, "black")
    screen.blit(score_text, (1100, 20))  # Display the score in the top right corner

    if game_over:
        # Game over screen
        screen.fill("#f0efef")
        font = pygame.font.Font(None, 50)
        game_over_text = font.render("Game Over!", True, "red")
        replay_button = pygame.Rect(550, 300, 180, 60)
        pygame.draw.rect(screen, "gray", replay_button)
        replay_text = font.render("Replay", True, "white")
        screen.blit(game_over_text, (550, 200))
        replay_text_rect = replay_text.get_rect(center=replay_button.center)
        screen.blit(replay_text, replay_text_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
