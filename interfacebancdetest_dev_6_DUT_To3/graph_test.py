
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import csv
import seaborn as sns
from datetime import datetime



sns.set_style("darkgrid")

x=[]
y=[]

i=1

with open('data_dut_2_2019-2-22-17-34-36.csv', 'r') as csvfile:
    plots= csv.reader(csvfile, delimiter=';')
    next(plots)
    ymax=max()
    for row in plots:
        y.append(float((row[1]).replace(',','.')))
        date=datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S.%f')
        x.append(date)

        i+=1


#plt.plot(x,y, marker=',')

f, (ax, ax2) = plt.subplots(2, 1, sharex=True)
ax.plot(x,y,  linewidth=1)
ax2.plot(x,y,  linewidth=1)

# zoom-in / limit the view to different portions of the data
ax.set_ylim(200, 1000)  # outliers only
ax2.set_ylim(0, .12)  # most of the data

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

plt.savefig('test_init_0_1.pdf', dpi=1000)





