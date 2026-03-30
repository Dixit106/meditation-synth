#trying to generate sin wave
#importing part
import pygame 
import numpy 
import math 
import time

bits = 16
sample_rate = 44100
pygame.mixer.pre_init(sample_rate, -bits, 2)
pygame.init()

#formula thing for sin wave
def sin_x(amp, freq, time):
    return int(round(amp * math.sin(2 * math.pi * freq * time)))

#tone class
class Tone:
    @staticmethod 
    def sine(freq, duration=1, speaker=None):

        num_samples = int(round(duration * sample_rate))

        sound_buffer = numpy.zeros((num_samples, 2), dtype = numpy.int16)
        amplitude = 2 ** (bits - 1) - 1

        for sample_num in range(num_samples):
            t = float(sample_num) / sample_rate

            #generating x cordinate
            sine = sin_x(amplitude, freq, t)

            if speaker == 'r':
                sound_buffer[sample_num][1] = sine 
            if speaker == 'l':
                sound_buffer[sample_num][0] = sine 
            else:
                sound_buffer[sample_num][1] = sine 
                sound_buffer[sample_num][0] = sine        

        sound = pygame.sndarray.make_sound(sound_buffer)
        sound.play(loops=1, maxtime=int(duration * 1000))
        time.sleep(duration)        