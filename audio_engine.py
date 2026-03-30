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
    def sine(freq, duration=1, speaker=None):
        #max volume for 16 bit audio
        amplitude = 2 ** (bits - 1) - 1

        #to generate time array using numpy
        t = numpy.linspace(0, duration, int(sample_rate * duration), False)

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
            sound_buffer[:, 1] = wave # for both        

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