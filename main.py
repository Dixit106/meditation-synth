#importing stuff
import pygame 
import sys 
from audio_engine import Tone 

#keyboard button press option
pygame.init()
screen = pygame.display.set_mode((500, 400))
pygame.display.set_caption("Meditation Audio Engine")

print("--- Solfeggio Frequencies ---")
print("Press 1: Sine[432Hz (Calm)] | 2: Square[528Hz (Repair)] | 3: 639Hz(Connection) | ")
print("--- Noise ---")
print("Press 4: White Noise (static) | 5: Brown Noise (Focus) | ")
print("--- Brainwaves (Binaural) --- [WEAR HEADPHONES!!!]")
print("Press 6: Alpha (Light Focus) | 7: Theta (Deep Meditation)")
print("SPACE: Stop | Close window to quit.")

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
                #Square
            elif event.key == pygame.K_2:
                print("Playing Square[528Hz (Repair Frequency)]...")
                Tone.square(528)
                #639Hz
            elif event.key == pygame.K_3:
                print("Playing 638Hz (Connection)...")
                Tone.sine(628)
                #White Noise
            elif event.key == pygame.K_4:
                print("Playing Pure White Noise (Static)...")
                Tone.white_noise()
                #Brown Noise 
            elif event.key == pygame.K_5:
                print("Playing Brown Noise (Focus)...")
                Tone.brown_noise()
                #Binaural Beats
            elif event.key == pygame.K_6:
                print("Playing Alpha Binaural (200Hz base + 10Hz beat)...")
                Tone.binaural_beat(200, 10)
            elif event.key == pygame.K_7:
                print("Playing Theta Binaural (200Hz base + 5Hz beat)...")
                Tone.binaural_beat(200, 5)
            elif event.key == pygame.K_SPACE:
                print("Stopping audio.")
                Tone.stop()            

Tone.stop()
pygame.quit()
sys.exit()
