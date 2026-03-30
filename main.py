#importing stuff
import pygame 
import sys 
from audio_engine import Tone 

#keyboard button press option
pygame.init()
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Synth Test Window")

print("Press 1 for Sine, 2 for Square, 3 for Noise. Close window to quit.")

running = True 
while running:
    for event in pygame.event.get():
        #will let window close properly
        if event.type == pygame.QUIT:
            running = False 

        #This to see which key is pressed
        if event.type == pygame.KEYDOWN:   
            if event.key == pygame.K_1:
                print("Playing Sine...")
                Tone.sine(440, duration=1)
            elif event.key == pygame.K_2:
                print("Playing Square...")
                Tone.square(440, duration=1)        

pygame.quit()
sys.exit()
