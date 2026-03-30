#importing stuff
import pygame 
import sys 
from audio_engine import Tone 

#keyboard button press option
pygame.init()
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Infinite Audio Test")

print("Press 1 for Sine[432Hz (Calm)], 2 for Square[528Hz (Repair)], 3 for Pure White Noise(static), SPACE: Stop. Close window to quit.")

running = True 
while running:
    for event in pygame.event.get():
        #will let window close properly
        if event.type == pygame.QUIT:
            running = False 

        #This to see which key is pressed
        if event.type == pygame.KEYDOWN:   
            if event.key == pygame.K_1:
                print("Playing Sine[432Hz (Calming Frequency)]...")
                Tone.sine(432)
            elif event.key == pygame.K_2:
                print("Playing Square[528Hz (Repair Frequency)]...")
                Tone.square(528)
            elif event.key == pygame.K_3:
                print("Playing Pure White Noise(Static)...")
                Tone.white_noise()    
            elif event.key == pygame.K_SPACE:
                print("Stopping audio.")
                Tone.stop()            

Tone.stop()
pygame.quit()
sys.exit()
