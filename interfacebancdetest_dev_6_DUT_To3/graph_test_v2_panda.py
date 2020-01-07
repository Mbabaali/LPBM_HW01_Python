
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import csv
import seaborn as sns
from datetime import datetime
import pandas as pd



sns.set_style("darkgrid")

df=pd.read_csv('data_dut_2_2019-2-26-16-28-5.csv', sep=";", decimal=',')




y=df['Value']

x=df['date-time']
x=pd.to_datetime(df['date-time'], format='%Y-%m-%d %H:%M:%S.%f').astype(datetime)

y_low_min=y.min()-0.001
y_low_max=y.min()+0.1

y_high_max=y.max()+(y.max()*10/100)
y_high_min=y.max()-(y.max()*35/100)
print(y.min())
print(y.max())
print(y_low_min)
print(y_low_max)
print(y_high_min)
print(y_high_max)
print(y.idxmin())

# x=[]
# y=[]

# i=1

# with open('data_dut_2_2019-2-22-17-34-36.csv', 'r') as csvfile:
#     plots= csv.reader(csvfile, delimiter=';')
#     next(plots)
#     ymax=max()
#     for row in plots:
#         y.append(float((row[1]).replace(',','.')))
#         date=datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S.%f')
#         x.append(date)

#         i+=1




plt.plot(x,y, marker=',')

f, (ax, ax2) = plt.subplots(2, 1, sharex=True)
ax.plot(x,y,  linewidth=1)
ax2.plot(x,y,  linewidth=1)

# zoom-in / limit the view to different portions of the data
ax.set_ylim(y_high_min, y_high_max)  # outliers only
ax2.set_ylim(y_low_min, y_low_max)  # most of the data

# hide the spines between ax and ax2
ax.spines['bottom'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax.xaxis.tick_top()
ax.tick_params(labeltop='off')  # don't put tick labels at the top
ax2.xaxis.tick_bottom()

d = .015  # how big to make the diagonal lines in axes coordinates
# arguments to pass to plot, just so we don't keep repeating them
kwargs = dict(transform=ax.transAxes, color='k', clip_on=False)
ax.plot((-d, +d), (-d, +d), **kwargs)        # top-left diagonal
ax.plot((1 - d, 1 + d), (-d, +d), **kwargs)  # top-right diagonal

kwargs.update(transform=ax2.transAxes)  # switch to the bottom axes
ax2.plot((-d, +d), (1 - d, 1 + d), **kwargs)  # bottom-left diagonal
ax2.plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)  # bottom-right diagonal


f.suptitle('Data from the CSV File: conso en mA')

plt.xlabel('Date')
plt.ylabel('Conso (en mA)')

plt.savefig('test_init_0_1_vpanda.pdf', dpi=1000)





