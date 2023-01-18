"""
Example for creating axes and updating text in an axes.
"""
import matplotlib.pyplot as plt
import numpy as np
import random
from src.biosim.map import Map





fig = plt.figure()
ax1 = fig.add_subplot(2, 3, 1)
ax2 = fig.add_subplot(2, 3, 3)
ax3 = fig.add_subplot(2, 3, 4)
ax4 = fig.add_subplot(2, 3, 5)
ax5 = fig.add_subplot(2, 3, 6)

# axes for text
axt = fig.add_axes([0.4, 0.8, 0.2, 0.2])  # llx, lly, w, h
axt.axis('off')  # turn off coordinate system
template = 'Year: {:5d}'
txt = axt.text(0.5, 0.5, template.format(0),
               horizontalalignment='center',
               verticalalignment='center',
               transform=axt.transAxes)  # relative coordinates

# plt.pause(0.01)  # pause required to make figure visible
#
# input('Press ENTER to begin counting')

max_step = 300
step_size = 1
ax2.set_title('Carnivore/Herbivore Pop:')
ax2.set_xlim(0, max_step)
ax2.set_ylim(0, 100)
xdata = np.arange(0, max_step, step_size)
line = ax2.plot(xdata, np.full_like(xdata, np.nan, dtype=float), 'b-')[0]
random.seed(12345)
year_num=5
car_num=5
# for n in range(0, max_step, step_size):
txt.set_text(template.format(year_num))
idx = year_num // step_size  # integer division to get correct array location
ydata = line.get_ydata()
ydata[idx] = 5
print(car_num)
line.set_ydata(ydata)
plt.pause(0.1)  # pause required to make update visible

plt.show()
