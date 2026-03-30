#trying to generate sin wave
#importing part
import pygame 
import numpy 
import math 
import time

#audio quality
bits = 16
sample_rate = 44100
pygame.mixer.pre_init(sample_rate, -bits, 2)
pygame.init()


#tone class
class Tone:

    @staticmethod 
    def stop():
        #This will stop any sounds currently playing
        pygame.mixer.stop()

    @staticmethod 
    def sine(freq, speaker=None):
        Tone.stop() #will stop old sound before new one
        #max volume for 16 bit audio
        amplitude = 2 ** (bits - 1) - 1

        #to generate time array using numpy
        t = numpy.linspace(0, 1,sample_rate, False)

        # formula thing for sine wave
        wave = amplitude * numpy.sin(2 * numpy.pi * freq * t)

        #making stereo buffer
        sound_buffer = numpy.zeros((len(wave), 2), dtype=numpy.int16)

        #speaker logic
        if speaker == 'r':
            sound_buffer[:, 1] = wave # for right
        elif speaker == 'l':
            sound_buffer[:, 0] = wave # for left
        else:
            sound_buffer[:, 0] = wave # for both 
            sound_buffer[:, 1] = wave # for both

        #play the sound
        sound = pygame.sndarray.make_sound(sound_buffer)
        sound.play(loops=-1) # -1 makes it play forever   

        
    @staticmethod
    def square(freq, duration=1, speaker=None):
        #volume lowered so it won't hurt ears
        amplitude = (2 ** (bits - 1) -1) * 0.5

        #time array
        t = numpy.linspace(0, duration, int(sample_rate * duration), False)

        #formula for square wave
        wave = amplitude * numpy.sign(numpy.sin(2 * numpy.pi * freq * t))

        #making stereo buffer(same as above)
        sound_buffer = numpy.zeros((len(wave), 2), dtype=numpy.int16)

        if speaker == 'r':
            sound_buffer[:, 1] = wave
        elif speaker == 'l':
            sound_buffer[:, 0] = wave 
        else:
            sound_buffer[:, 0] = wave 
            sound_buffer[:, 1] = wave

        sound = pygame.sndarray.make_sound(sound_buffer)
        sound.play(loops=-1)                       

    @staticmethod
    def white_noise(duration=1, speaker=None):
        #volume lowered more for noise
        amplitude = (2 ** (bits - 1) -1) * 0.3

        num_samples = int(sample_rate * duration)

        #random noise formula
        wave = numpy.random.uniform(-amplitude, amplitude, num_samples)

        #making stereo buffer again
        sound_buffer = numpy.zeros((len(wave), 2), dtype=numpy.int16)

        if speaker == 'r':
            sound_buffer[:, 1] = wave 
        elif speaker == 'l':
            sound_buffer[:, 0] = wave 
        else:
            sound_buffer[:, 0] = wave 
            sound_buffer[:, 1] = wave 

        sound = pygame.sndarray.make_sound(sound_buffer)
        sound.play(loops=-1)