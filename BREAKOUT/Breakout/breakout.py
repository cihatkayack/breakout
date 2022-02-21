"""
File: breakout.py
-----------------
This program implements the game Breakout!  The user controls a paddle
moving horizontally with the mouse, and the user must bounce the ball
to make it collide and remove bricks from the screen.  The user has
3 turns.  If the ball falls below the bottom of the screen, the user
loses a turn.  If the user removes all bricks before their turns
run out, they win!
"""

import math
from graphics import Canvas
import random
import time

"""
Dimensions of the canvas, in pixels
These should be used when setting up the initial size of the game,
but in later calculations you should use canvas.get_canvas_width() and 
canvas.get_canvas_height() rather than these constants for accurate size information.
"""
canvas = Canvas()

CANVAS_WIDTH = 420
CANVAS_HEIGHT = 600

# Stage 1: Set up the Bricks

# Number of bricks in each row
NBRICK_COLUMNS = 10

# Number of rows of bricks
NBRICK_ROWS = 10

# Separation between neighboring bricks, in pixels
BRICK_SEP = 4

# Width of each brick, in pixels
BRICK_WIDTH = math.floor((CANVAS_WIDTH - (NBRICK_COLUMNS + 1.0) * BRICK_SEP) / NBRICK_COLUMNS)

# Height of each brick, in pixels
BRICK_HEIGHT = 8

# Offset of the top brick row from the top, in pixels
BRICK_Y_OFFSET = 70

# Stage 2: Create the Bouncing Ball

# Radius of the ball in pixels
BALL_RADIUS = 10

# The ball's vertical velocity.
VELOCITY_Y = 8.0

# The ball's minimum and maximum horizontal velocity; the bounds of the
# initial random velocity that you should choose (randomly +/-).
VELOCITY_X_MIN = 2.0
VELOCITY_X_MAX = 6.0

# Animation delay or pause time between ball moves (in seconds)
DELAY = 1 / 60

# Stage 3: Create the Paddle

# Dimensions of the paddle
PADDLE_WIDTH = 60
PADDLE_HEIGHT = 10

# Offset of the paddle up from the bottom
PADDLE_Y_OFFSET = 30

# Stage 5: Polish and Finishing Up

# Number of turns
NTURNS = 3

BOUNCE_SOUND = "bounce.au"

BRICK_LIST = []

def restart_game(canvas):
    BRICK_LIST.clear()
    restartGame = 1
    while restartGame == 1:
        restart = canvas.get_new_key_presses()
        for press in restart:
            if press.keysym == "space":
                canvas.delete_all()
                restartGame = 0
                main()
            time.sleep(DELAY)
        time.sleep(DELAY)
        canvas.update()
    

def create_bricks_layout(canvas):
    count = 0
    for i in range(NBRICK_ROWS):
        for j in range(NBRICK_COLUMNS):
            create_bricks(canvas, i, j, count)
            count += 1
            
            
            
def create_bricks(canvas, i, j, count):
    colors = ["red", "orange", "yellow","green", "cyan"]
    color = count // 20
    y = i * (BRICK_HEIGHT + BRICK_SEP)
    x = j * (BRICK_WIDTH + BRICK_SEP)
    
    BRICK_LIST.append(canvas.create_rectangle(x, BRICK_Y_OFFSET + y, x + BRICK_WIDTH,BRICK_Y_OFFSET + y + BRICK_HEIGHT))
    
    canvas.set_color(BRICK_LIST[count], colors[color])

def create_ball(canvas, w, h):
    ball = canvas.create_oval((w / 2) - BALL_RADIUS, (h / 2) - BALL_RADIUS,
                              (w / 2) + BALL_RADIUS, (h / 2) + BALL_RADIUS)
    canvas.set_color(ball, "black")
    return ball

def animation_ball(canvas, ball, ball_velocity_x, ball_velocity_y):
    
    canvas.move(ball, ball_velocity_x, ball_velocity_y)
    

def create_paddle(canvas, w, h):
    paddle = canvas.create_rectangle((w / 2) - (PADDLE_WIDTH/2), h - (PADDLE_Y_OFFSET + PADDLE_HEIGHT),
                                     (w / 2) + (PADDLE_WIDTH/2), h - PADDLE_Y_OFFSET)
    canvas.set_color(paddle, "black")
    
    return paddle

def animation_paddle(canvas, mouse_x, paddle):
    y = canvas.get_top_y(paddle)
    canvas.moveto(paddle, mouse_x, y)



def collision(canvas,ball,paddle):
    is_collided_paddle = False
    
    is_collided_brick = False
    
    ball_coords = canvas.coords(ball)
    
    colliders = canvas.find_overlapping(ball_coords[0],ball_coords[1], ball_coords[2], ball_coords[3])
    
    if paddle in colliders:
        is_collided_paddle = True
    
    elif len(colliders) > 1:
        is_collided_brick= True
        
        for i in colliders:
            if i == ball:
                continue
            else:
                canvas.delete(i)
                BRICK_LIST.remove(i)
    
        
    
    return is_collided_paddle,is_collided_brick 
    

def create_start_screen(canvas, w, h):
    

    sentence = "CLICK SOMEWHERE TO START"
    text = canvas.create_text(w/2, h/2 + 50, sentence)
    canvas.set_font(text, "Courier", 17)
    canvas.set_color(text, "black")

    return text

def determine_lives_number(canvas, w, h, lives):
    text = canvas.create_text(w/2, h/2 + 100, "")
    text_for_screen = canvas.set_text(text, "Lives: " + str(lives))
    canvas.set_font(text, "Courier", 17)
    canvas.set_color(text, "black")
    
    return text

def main():
    canvas.set_canvas_size(CANVAS_WIDTH, CANVAS_HEIGHT)
    canvas.set_canvas_title("Breakout")
    turns = NTURNS
    w = CANVAS_WIDTH
    h = CANVAS_HEIGHT
    start_text = create_start_screen(canvas, w, h)
    lives = determine_lives_number(canvas, w, h, turns)
    create_bricks_layout(canvas)
    ball = create_ball(canvas, w, h)
    paddle = create_paddle(canvas, w, h)
    ball_velocity_x = random.randint(VELOCITY_X_MIN, VELOCITY_X_MAX)
    ball_velocity_y = VELOCITY_Y 
    canvas.wait_for_click()
    canvas.delete(start_text)
    canvas.delete(lives)
    while True:
        
        animation_ball(canvas, ball, ball_velocity_x, ball_velocity_y)
        if canvas.get_left_x(ball) <= 0 :
            ball_velocity_x = - ball_velocity_x
        if canvas.get_left_x(ball) >= canvas.get_canvas_width() - canvas.get_width(ball):
            ball_velocity_x = - ball_velocity_x
        if canvas.get_top_y(ball) <= 0:
            ball_velocity_y = - ball_velocity_y
        if canvas.get_top_y(ball) >= canvas.get_canvas_height() + canvas.get_height(ball):
            turns -= 1
            if turns == 0:
                sentence_for_lives = "GAME OVER"
                text_for_lives = canvas.create_text(w/2, h/2, sentence_for_lives)
                canvas.set_font(text_for_lives, "Courier", 50)
                canvas.set_color(text_for_lives, "black")
                sentence = "PRESS 'SPACE' FOR RESTART"
                text = canvas.create_text(w/2, h/1.3 + 50, sentence)
                canvas.set_font(text, "Courier", 17)
                canvas.set_color(text, "black")
                restart_game(canvas)
            canvas.delete(ball)
            ball = create_ball(canvas, w, h)
            start_text = create_start_screen(canvas, w, h)
            lives = determine_lives_number(canvas, w, h, turns)
            canvas.wait_for_click()
            canvas.delete(start_text)
            canvas.delete(lives)
            
            
            
        mouse_x = canvas.get_mouse_x() - PADDLE_WIDTH / 2
        if mouse_x >= 0 and mouse_x + PADDLE_WIDTH <= w:
            animation_paddle(canvas, mouse_x, paddle)
        
        if collision(canvas, ball, paddle)[1]:
            ball_velocity_y = -ball_velocity_y 
            
            
        if collision(canvas, ball, paddle)[0]:
            ball_velocity_y = -ball_velocity_y
        
        if BRICK_LIST == []:
            sentence = "WIN"
            text = canvas.create_text(w/2, h/2, sentence)
            canvas.set_font(text, "Courier", 50)
            canvas.set_color(text, "black")
            sentence_for_restart = "PRESS 'SPACE' FOR RESTART"
            text_for_restart = canvas.create_text(w/2, h/1.3 + 50, sentence_for_restart)
            canvas.set_font(text_for_restart, "Courier", 17)
            canvas.set_color(text_for_restart, "black")
            restart_game(canvas)
            canvas.update()
            
        
        canvas.update()
        time.sleep(DELAY)
    # TODO: your code here!

    canvas.mainloop()


if __name__ == '__main__':
    main()
