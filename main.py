'''
Simulación de colisiones de bolas de billar

UNAM ENES Unidad Morelia
Modelado y simulación

José Ignacio Esparza Ireta
Mario Alberto Martínez Oliveros
'''

# Libraries and modules
import pygame
import pymunk

# Functions
def to_pygame(p):
    '''
    Function to convert pymunk coordinates to pygame coordinates
    '''

    return int(p.x), int(-p.y + 600)

def ball_collision_handler_func(arbiter, space, data):
    '''
    Function to handle ball collisions
    '''

    print("Balls collided!")
    return True

def cue_collision_handler_func(arbiter, space, data):
    '''
    Function to handle cue collisions
    '''

    direction_vector = arbiter.shapes[0].body.position - arbiter.shapes[1].body.position    # Calculate the direction and magnitude of the force
    direction = direction_vector / direction_vector.length                                  # Normalize the direction vector
    force = direction * 1000                                                                # Adjust the magnitude as needed

    arbiter.shapes[0].body.apply_impulse_at_local_point(force)                              # Apply the force to the ball

    return False

def edge_collision_handler_func(arbiter, space, data):
    '''
    Function to handle edge collisions
    '''

    print("Ball collided with table edge!")
    return True

# Initalize the game engine
pygame.init()               # Initialize Pygame
space = pymunk.Space()      # Create a Space which contain the simulation
space.gravity = (0.0, 0.0)  # Set gravity

# Add the ball collision handler
ball_collision_handler = space.add_collision_handler(1, 1)
ball_collision_handler.begin = ball_collision_handler_func

# Add the cue collision handler
cue_collision_handler = space.add_collision_handler(1, 3)
cue_collision_handler.begin = cue_collision_handler_func

# Add the edge collision handler
edge_collision_handler = space.add_collision_handler(1, 2)
edge_collision_handler.begin = edge_collision_handler_func

# Create the balls
balls = []

for i in range(3):
    for j in range(i+1):
        ball_body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, 20, (0, 0))) # Create the ball body
        ball_body.position = 400 + i * 30, 300 + j * 30 - i * 15               # Adjust the ball position
        ball_shape = pymunk.Circle(ball_body, 20)                              # Create the ball shape
        space.add(ball_body, ball_shape)                                       # Add the ball to the space
        balls.append(ball_shape)                                               # Add the ball to the list of balls

# Create the cue ball
cue_ball_body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, 20, (0, 0)))     # Create the cue ball body
cue_ball_body.position = 250, 300                                              # Position it in front of the center ball
cue_ball_shape = pymunk.Circle(cue_ball_body, 20)                              # Create the cue ball shape
cue_ball_shape.collision_type = 1                                              # Set the collision type
space.add(cue_ball_body, cue_ball_shape)                                       # Add the cue ball to the space
balls.append(cue_ball_shape)                                                   # Add the cue ball to the list of balls

# Create the cue stick
cue_stick_body = pymunk.Body(body_type = pymunk.Body.KINEMATIC)                # Create the cue stick body
cue_stick_body.position = 50, 300                                              # Position it to the left of the cue ball
cue_stick_shape = pymunk.Segment(cue_stick_body, (0, 0), (100, 0), 5)          # Increase the size
cue_stick_shape.collision_type = 3                                             # Set the collision type
space.add(cue_stick_body, cue_stick_shape)                                     # Add the cue stick to the space

# Create the pool table edges
static_lines = [pymunk.Segment(space.static_body, (50, 50), (550, 50), 5),     # Bottom edge
                pymunk.Segment(space.static_body, (50, 550), (550, 550), 5),   # Top edge
                pymunk.Segment(space.static_body, (50, 50), (50, 550), 5),     # Left edge
                pymunk.Segment(space.static_body, (550, 50), (550, 550), 5)]   # Right edge

for line in static_lines:
    line.elasticity = 0.95                                                     # Make the balls bounce off the edges
    line.friction = 0.9                                                        # Add some friction
    line.collision_type = 2                                                    # Set the collision type
    space.add(line)                                                            # Add the edge to the space

# Create the screen
screen = pygame.display.set_mode((600, 600))                                   # Set the screen size
clock = pygame.time.Clock()                                                    # Create a clock to control the frame rate

# Game loop
running = True
while running:

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                cue_stick_body.position = pymunk.Vec2d(cue_stick_body.position.x - 10, cue_stick_body.position.y)  # Move left

            elif event.key == pygame.K_RIGHT:
                cue_stick_body.position = pymunk.Vec2d(cue_stick_body.position.x + 10, cue_stick_body.position.y)  # Move right

    # Clear the screen
    screen.fill((0, 255, 0))

    # Draw the pool table edges
    for line in static_lines:
        body = line.body                                            # Get the line body
        pv1 = body.position + line.a.rotated(body.angle)            # Begin point
        pv2 = body.position + line.b.rotated(body.angle)            # End point
        p1 = to_pygame(pv1)                                         # Convert to Pygame coordinates
        p2 = to_pygame(pv2)                                         # Convert to Pygame coordinates
        pygame.draw.lines(screen, (255, 255, 255), False, [p1, p2]) # Draw the line

    # Draw the balls
    for ball in balls:
        pos = ball.body.position                                                        # Get the ball position
        pygame.draw.circle(screen, (255, 255, 255), (int(pos.x), int(600 - pos.y)), 20) # Draw the ball
        
    # Draw the cue stick
    for line in [cue_stick_shape] + static_lines:
        body = line.body                                      # Get the line body
        pv1 = body.position + line.a.rotated(body.angle)      # Begin point
        pv2 = body.position + line.b.rotated(body.angle)      # End point
        p1 = to_pygame(pv1)                                   # Convert to Pygame coordinates
        p2 = to_pygame(pv2)                                   # Convert to Pygame coordinates
        pygame.draw.lines(screen, (0, 0, 0), False, [p1, p2]) # Draw the line

    # Update the physics
    space.step(1/60.0)

    # Update the display
    pygame.display.flip()
    clock.tick(60)

# Quit Pygame
pygame.quit()
