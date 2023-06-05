import pygame
import random
import numpy as np
import matplotlib.pyplot as plt

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

num_episodes = 1
total_reward = 0

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
    obstacle_y = 440


spawn_obstacle()

# Q-learning parameters
alpha = 0.7  # Learning rate
gamma = 0.9  # Discount factor
epsilon = 0.1  # Exploration rate

# Q-table
num_states = 2  # Number of states (actions: jump or duck)
num_distances = 1280  # Number of possible distances (based on the screen width)
num_actions = 2  # Number of actions (0: do nothing, 1: jump, 2: duck)
q_table = np.zeros((num_states, num_distances, num_actions))

episode_numbers = []
total_rewards = []


def choose_action(state, distance):
    if random.uniform(0, 1) < epsilon:
        # Explore: choose a random action
        return random.randint(0, num_actions - 1)
    else:
        # Exploit: choose the action with the highest Q-value for the current state
        return np.argmax(q_table[state, distance])


def get_distance():
    return obstacle_x - player_x


def update_q_table(state, action, reward, distance):
    global game_over

    if game_over:
        # Apply penalty for dying
        reward = -100

    # Update Q-value for the previous state-action pair using the Q-learning formula
    q_table[state, distance, action] = (1 - alpha) * q_table[state, distance, action] + alpha * (
            reward + gamma * np.max(q_table[state, distance]))


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
    global score, add_score, total_reward

    if obstacle_x < player_x and add_score:
        update_q_table(state, action, 50, next_state)
        total_reward += 1
        score += 50
        add_score = False


def display_episode_results(episode_number, total_reward):
    # Append the episode number and total reward to the lists
    episode_numbers.append(episode_number)
    total_rewards.append(total_reward)

    # Clear the previous plot and create a new one
    plt.figure()

    # Plot the data
    plt.plot(episode_numbers, total_rewards, label='Episode Results')

    # Fit a polynomial regression line
    trend = np.polyfit(episode_numbers, total_rewards, deg=1)
    trend_line = np.poly1d(trend)
    plt.plot(episode_numbers, trend_line(episode_numbers), color='red', label='Trend Line')

    plt.xlabel('Number of Episodes')
    plt.ylabel('Total Reward')
    plt.title('Episode Results')
    plt.legend()

    # Display the plot
    plt.show()


def restart_game():
    global on_ground, ascending, jump_speed, player_height, player_y, game_over, score, add_score, num_episodes, total_reward
    display_episode_results(num_episodes, total_reward)
    on_ground = True
    ascending = False
    jump_speed = 0
    player_height = full_height
    player_y = 400
    game_over = False
    score = 0
    add_score = True
    num_episodes += 1
    total_reward = 0
    spawn_obstacle()


def update_obstacle():
    global obstacle_x, add_score

    obstacle_x -= obstacle_speed

    if obstacle_x <= 0:
        add_score = True
        spawn_obstacle()


learning_status_font = pygame.font.Font(None, 24)  # Font for displaying the learning status


def display_statistics():
    statistics_text = [f"Episodes: {num_episodes}", f"Total Reward: {total_reward}", f"Distance: {get_distance()}"]
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
        action = choose_action(state, get_distance())

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
        reward = 1  # Placeholder for the reward
        update_q_table(state, action, reward, get_distance())

    display_statistics()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
