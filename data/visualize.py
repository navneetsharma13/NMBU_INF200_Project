import pandas as pd
import numpy as np
from pathlib import Path
import re
import matplotlib.pyplot as plt

plt.rcParams['figure.figsize'] = (20, 30)

data = []


for logfile in Path().glob('mono_hc_*.csv'):
    d = pd.read_csv(logfile, skiprows=1, usecols=[0, 1], index_col=0,
                names=['Year', 'Herbivores'])
    #print(d)
    d['Seed'] = int(re.match(r'.*_(\d+)\.csv', str(logfile)).group(1))
    #print(d)
    data.append(d)
    #print(data)
hd = pd.concat(data).pivot(columns='Seed')
hd.head()
#print(hd)
hd.Herbivores.plot(legend=False, alpha=0.5);
plt.show()

hd_eq = hd.loc[hd.index >= 100, :]
print(hd_eq.mean())

print(hd_eq.std())

print(hd_eq.unstack().mean())

print(hd_eq.unstack().std())

bins = np.arange(160, 240, 2)
plt.hist(hd_eq.Herbivores.unstack(), bins=bins, fc='b', histtype='stepfilled', alpha=0.4);
#plt.show()