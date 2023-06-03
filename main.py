import pygame
import random
import numpy as np

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

replay_button = pygame.Rect(550, 300, 180, 60)


def spawn_obstacle():
    global obstacle_x, obstacle_y
    obstacle_x = 1240
    obstacle_y = random.choice([380, 440])


spawn_obstacle()

# Q-learning parameters
alpha = 0.1  # Learning rate
gamma = 0.9  # Discount factor
epsilon = 0.1  # Exploration rate

# Q-table
num_states = 2  # Number of states (actions: jump or duck)
num_actions = 3  # Number of actions (0: do nothing, 1: jump, 2: duck)
q_table = np.zeros((num_states, num_actions))


def choose_action(state):
    if random.uniform(0, 1) < epsilon:
        # Explore: choose a random action
        return random.randint(0, num_actions - 1)
    else:
        # Exploit: choose the action with the highest Q-value for the current state
        return np.argmax(q_table[state])


def update_q_table(state, action, reward, next_state):
    # Update Q-value for the previous state-action pair using the Q-learning formula
    q_table[state, action] = (1 - alpha) * q_table[state, action] + alpha * (
            reward + gamma * np.max(q_table[next_state]))


def perform_action(action):
    global on_ground, ascending, jump_speed, player_height, player_y

    if action == 1 and on_ground:
        on_ground = False
        ascending = True
        jump_speed = -10
    elif action == 2 and on_ground:
        player_height = duck_height
        player_y = 440
    elif on_ground:
        player_height = full_height
        player_y = 400


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
        restart_game()


def update_score():
    global score, add_score

    if obstacle_x < player_x and add_score:
        score += 50
        add_score = False


def restart_game():
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


def update_obstacle():
    global obstacle_x

    obstacle_x -= obstacle_speed

    if obstacle_x <= 0:
        add_score = True
        spawn_obstacle()


learning_status_font = pygame.font.Font(None, 24)  # Font for displaying the learning status

num_episodes = 0
total_reward = 0

def display_statistics():
    statistics_text = []
    statistics_text.append(f"Episodes: {num_episodes}")
    statistics_text.append(f"Total Reward: {total_reward}")
    # Add more statistics as needed

    x = 10
    y = 40
    line_height = 24

    for stat in statistics_text:
        stat_text = learning_status_font.render(stat, True, (0, 0, 0))
        screen.blit(stat_text, (x, y))
        y += line_height



while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("#f0efef")

    if not game_over:
        # Get the current state based on the player's position and whether they are on the ground or not
        state = int(on_ground)

        # Choose an action based on the current state
        action = choose_action(state)

        update_obstacle()

        # Perform the chosen action
        perform_action(action)

        # Update the game state
        update_game_state()

        # Check for collision with obstacle
        check_collision()

        # Update the score
        update_score()

        player = pygame.Rect(player_x, player_y, player_width, player_height)
        obstacle = pygame.Rect(obstacle_x, obstacle_y, obstacle_width, obstacle_height)

        pygame.draw.rect(screen, "black", player)
        pygame.draw.rect(screen, "black", obstacle)

        # ... (rest of the code)

        # Update Q-table based on the current state, action, reward, and next state
        next_state = int(on_ground)
        reward = 0  # Placeholder for the reward
        update_q_table(state, action, reward, next_state)


    pygame.display.flip()
    clock.tick(60)

pygame.quit()
