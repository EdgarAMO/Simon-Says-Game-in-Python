# Simon Says
# Date: 1 / feb / 2021
# Author: Edgar A. M.

import pygame
import sys
import random
import time



""" Load images """
button_g_off = pygame.image.load('green_off.png')
button_y_off = pygame.image.load('yellow_off.png')
button_b_off = pygame.image.load('blue_off.png')
button_r_off = pygame.image.load('red_off.png')
buttons_off = {0:button_g_off, 1:button_y_off, 2:button_b_off, 3:button_r_off}

button_g_on = pygame.image.load('green_on.png')
button_y_on = pygame.image.load('yellow_on.png')
button_b_on = pygame.image.load('blue_on.png')
button_r_on = pygame.image.load('red_on.png')
buttons_on = {0:button_g_on, 1:button_y_on, 2:button_b_on, 3:button_r_on}

rectG = button_g_off.get_rect(center=(192, 192))
rectY = button_y_off.get_rect(center=(192, 320))
rectB = button_b_off.get_rect(center=(320, 320))
rectR = button_r_off.get_rect(center=(320, 192))
rects = {0:rectG, 1:rectY, 2:rectB, 3:rectR}

buttons = {0:button_g_off, 1:button_y_off, 2:button_b_off, 3:button_r_off}



""" Global objects """
sequence = []           # list of buttons that were displayed
click = 0               # count of clicks
wrong = False           # wrong click
state = 'OFF'           # state of the game



""" Buttons """
def simon_blinks(key):
    buttons[key] = buttons_on[key]

    # blit
    for i in buttons:
        screen.blit(buttons[i], rects[i])
        screen.blit(font.render(text, True, color), position) 
        pygame.display.update()

    # blink for 250ms
    time.sleep(0.25)

    # turn blinking button off
    screen.fill((30, 30, 30)) 
    buttons[key] = buttons_off[key]

    # blit
    for i in buttons:
        screen.blit(buttons[i], rects[i])
        screen.blit(font.render(text, True, color), position) 
        pygame.display.update()

    # pause between blinks for 750ms
    time.sleep(0.75)

def get_click(click_pos):

    global click
    global wrong
    
    for i in rects:
        if rects[i].collidepoint(click_pos):

            """ turn on clicked button """
            buttons[i] = buttons_on[i]
            # blit
            for j in buttons:
                screen.blit(buttons[j], rects[j])
                screen.blit(font.render(text, True, color), position) 
                pygame.display.update()

            # blink for 250ms
            time.sleep(0.25)

            # turn blinking button off
            screen.fill((30, 30, 30)) 
            buttons[i] = buttons_off[i]

            # blit
            for j in buttons:
                screen.blit(buttons[j], rects[j])
                screen.blit(font.render(text, True, color), position) 
                pygame.display.update()

            # pause between blinks for 750ms
            time.sleep(0.75)
            
            """ check whether the right button in the sequence was pressed """
            if i == sequence[click]:
                click += 1
            else:
                wrong = True                
    

    
""" Settings """

# pygame settings
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.mouse.set_visible(True)
clock = pygame.time.Clock()

# screen settings
W, H = 512, 512
screen = pygame.display.set_mode((W, H))
screen.fill((30, 30, 30))

# sequence keys settings
sequence.append( random.choice((0, 1, 2, 3)) )

# font settings
font = pygame.font.SysFont('FiraCode', 32)
score = 0
color = (255, 255, 255)
position = (160, 64)
text = str('Score: {}'.format(score))

# sound settings
beep = pygame.mixer.Sound('beep.wav')
laugh = pygame.mixer.Sound('laugh.wav')



""" Main Loop """
while 1:
    
    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        # Play sequence
        if state == 'OFF':
            for number in sequence:
                pygame.event.pump()
                beep.play()
                simon_blinks(number)
            state = 'ON'
            click = 0
        # Click buttons
        if state == 'ON':
            if event.type == pygame.MOUSEBUTTONDOWN:
                beep.play()
                get_click(pygame.mouse.get_pos())
            if wrong:
                text = 'Loser!'
                position = (192, 64)
                laugh.play()
                screen.fill((30, 30, 30))
                break
            if click == len(sequence):
                sequence.append( random.choice((0, 1, 2, 3)) )
                score += 1
                text = str('Score: {}'.format(score))
                screen.fill((30, 30, 30))
                state = 'OFF'

        

    # Drawing
    screen.blit(font.render(text, True, color), position)
    pygame.display.flip()
    clock.tick(60)
    
