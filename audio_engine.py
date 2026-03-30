#trying to generate sin wave
#importing part
import numpy as np
import math 
import matplotlib.pyplot as plt


time = np.arange(0,2*math.pi,math.pi/10)

amplitude = np.sin(time)
plt.plot(time,amplitude)
plt.show()