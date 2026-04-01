#trying to generate sin wave
#importing part
import sys 
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
    current_sound = None #This will be memory slot to hold the active sound

    @staticmethod 
    def set_volume(volume):
        #To turn volume knob down during the fade-out
        if Tone.current_sound:
            Tone.current_sound.set_volume(volume)

    @staticmethod 
    def stop():
        #This will stop any sounds currently playing
        pygame.mixer.stop()
        Tone.current_sound = None 
    
    #sine freq
    @staticmethod 
    def sine(freq, speaker=None):
        Tone.stop() #will stop old sound before new one
        #max volume for 16 bit audio
        amplitude = (2 ** (bits - 1) - 1) * 0.2 #tuning it more down so it won't hurt ears

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
        Tone.current_sound = pygame.sndarray.make_sound(sound_buffer)
        Tone.current_sound.set_volume(1.0)#Start at max volume
        Tone.current_sound.play(loops=-1) # -1 makes it play forever   

    #squre freq(i am not using this though used it initially)
    @staticmethod
    def square(freq, duration=1, speaker=None):
        Tone.stop() #will stop old sound before new one
        #volume lowered so it won't hurt ears
        amplitude = (2 ** (bits - 1) -1) * 0.1 #turned down even more

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

  #white noise
    @staticmethod
    def white_noise(duration=1, speaker=None):
        Tone.stop() #will stop old sound before new one
        #volume lowered more for noise
        amplitude = (2 ** (bits - 1) -1) * 0.1 #turned down to match others

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

        Tone.current_sound = pygame.sndarray.make_sound(sound_buffer)
        Tone.current_sound.set_volume(1.0)
        Tone.current_sound.play(loops=-1)

    #Pink Noise
    @staticmethod 
    def pink_noise(speaker=None):
        Tone.stop()
        #Volume at a safe middle ground
        amplitude = (2 ** (bits - 1) - 1) * 0.3

        num_samples = sample_rate * 5
        white = numpy.random.uniform(-1, 1, num_samples)

        freqs = numpy.fft.rfft(white)
        f_scale = numpy.arange(1,  len(freqs) + 1)

        #Pink noise math: divide by the square root of the frequency
        freqs = freqs / numpy.sqrt(f_scale)
        pink = numpy.fft.irfft(freqs)

        pink = pink / numpy.max(numpy.abs(pink)) * amplitude 

        sound_buffer = numpy.zeros((len(pink), 2), dtype=numpy.int16)

        #speaker thing again
        if speaker == 'r':
            sound_buffer[:, 1] = pink 
        elif speaker == 'l':
            sound_buffer[:, 0] = pink 
        else:
            sound_buffer[:, 0] = pink 
            sound_buffer[:, 1] = pink 

        Tone.current_sound = pygame.sndarray.make_sound(sound_buffer)
        Tone.current_sound.set_volume(1.0)
        Tone.current_sound.play(loops=-1)            





    #brown noise
    @staticmethod 
    def brown_noise(speaker=None):
        Tone.stop()
        amplitude = (2 ** (bits - 1) - 1) * 0.9 #turning up so we can hear it

        #will generate 5 seconds of noise
        num_samples = sample_rate * 5
        white = numpy.random.uniform(-1, 1, num_samples)

        #Math trick: BRown noise = sum of white noise so
        #Using Fast Fourier Transform will translate raw sound into frequency space
        freqs = numpy.fft.rfft(white)

        #array of no.  to divide the frequencies by
        f_scale = numpy.arange(1, len(freqs) + 1)

        #brown noise formula to divide frequencies by their positon (1/f)
        freqs = freqs / f_scale 

        #translating back to actual audio waves from frequency space
        brown = numpy.fft.irfft(freqs)
        
        #trying to remove distortion
        brown = brown / numpy.max(numpy.abs(brown)) * amplitude 

        sound_buffer = numpy.zeros((len(brown), 2), dtype=numpy.int16)

        #speaker thing
        if speaker == 'r':
            sound_buffer[:, 1] = brown
        elif speaker == 'l':
            sound_buffer[:,0] = brown 
        else:
            sound_buffer[:, 0] = brown 
            sound_buffer[:, 1] = brown 

        Tone.current_sound = pygame.sndarray.make_sound(sound_buffer)
        Tone.current_sound.set_volume(1.0)
        Tone.current_sound.play(loops=-1)                

       
        #binaural_beats
    @staticmethod 
    def binaural_beat(base_freq, beat_freq):
        Tone.stop()
        #Volume low for meditation
        amplitude = (2 ** (bits - 1) - 1) * 0.2

        t = numpy.linspace(0, 1, sample_rate, False)

        #Left ear gets the normal base frequency
        left_wave = amplitude * numpy.sin(2 * numpy.pi * base_freq * t)

        #right ear gets the base and the tiny beat difference
        right_wave = amplitude * numpy.sin(2 * numpy.pi * (base_freq + beat_freq) * t)

        sound_buffer = numpy.zeros((len(t), 2), dtype=numpy.int16)

        #exact waves for exact ears
        sound_buffer[:, 0] = left_wave #Left speaker
        sound_buffer[:, 1] = right_wave #Right speaker

        Tone.current_sound = pygame.sndarray.make_sound(sound_buffer)
        Tone.current_sound.set_volume(1.0)
        Tone.current_sound.play(loops=-1)