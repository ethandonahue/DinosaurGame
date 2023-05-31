import pygame

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

on_ground = True
ascending = False  # Flag to track if the player is ascending or descending

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("#f0efef")

    if not on_ground:
        if ascending:
            player_y += jump_speed  # Update player's position based on jump speed
            jump_speed += jump_acceleration  # Apply acceleration to the jump

            if player_y <= jump_target:
                ascending = False  # Change direction when reaching the jump target

        else:
            player_y += jump_speed  # Update player's position based on jump speed
            jump_speed += gravity  # Apply gravity during descending

    if player_y >= 400 and not on_ground:
        player_y = 400
        on_ground = True
        jump_speed = 0  # Reset jump speed when the player reaches the ground

    pygame.draw.rect(screen, "black", (player_x, player_y, player_width, player_height))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and on_ground:
        on_ground = False
        ascending = True  # Start ascending
        jump_speed = -10  # Start the jump by setting an initial jump speed
    if keys[pygame.K_s] and on_ground:
        player_height = duck_height
        player_y = 440
    elif on_ground:
        player_y = 400
        player_height = full_height

    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
