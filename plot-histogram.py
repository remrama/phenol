"""
Plot a single histogram counting responses
per lucidity level across all participants.
"""

from os import path
import pandas as pd

import matplotlib; matplotlib.use('Qt5Agg') # python3 bug
import matplotlib.pyplot as plt; plt.ion()

import pyplotparams as myplt

datadir = path.expanduser('~/IDrive-Sync/proj/phenol/data')
resdir  = path.expanduser('~/IDrive-Sync/proj/phenol/results')

infname = path.join(datadir,'data-clean.tsv')
outfname = path.join(resdir,'dlq1-histogram.png')


########  load and manipulate data  ########

df = pd.read_csv(infname,sep='\t')

all_markers = list(matplotlib.markers.MarkerStyle.filled_markers)
subjs = df['subj'].unique().tolist()



xvals = []
yvals = []
markers = []
counts = { x: 1 for x in [1,2,3,4,5] }

for _, row in df.iterrows():
    resp = row['DLQ:1']
    if not pd.np.isnan(resp):
        subj = row['subj']
        mark = all_markers[subjs.index(subj)]
        yval = counts[resp]
        counts[resp] += 1

        xvals.append(resp)
        yvals.append(yval)
        markers.append(mark)



##########  draw it  ###########

fig, ax = plt.subplots(figsize=(4,7))

# for x, y, m in zip(xvals,yvals,markers):
#     c = myplt.dlqcolor(x)
#     ax.scatter(x,y,color=c,marker=m,edgecolors='k',linewidths=.5,s=85)

ax.bar(1,24,edgecolor='k',width=1,linewidth=.5,color=myplt.dlqcolor(1))#,zorder=0,alpha=.8)
ax.bar(2,11,edgecolor='k',width=1,linewidth=.5,color=myplt.dlqcolor(2))#,zorder=0,alpha=.8)
ax.bar(3,4, edgecolor='k',width=1,linewidth=.5,color=myplt.dlqcolor(3))#,zorder=0,alpha=.8)
ax.bar(4,9, edgecolor='k',width=1,linewidth=.5,color=myplt.dlqcolor(4))#,zorder=0,alpha=.8)
ax.bar(5,4, edgecolor='k',width=1,linewidth=.5,color=myplt.dlqcolor(5))#,zorder=0,alpha=.8)

ax.set_xlim(.25,5.75)
ax.set_ylim(0,max(yvals)+1)
# ax.set_yticks(range(0,max(yvals)))
ax.set_xticks([1,2,3,4,5])
ax.set_xticklabels(list(myplt.DLQ_STRINGS.values()),rotation=25)
ax.set_ylabel('Number of nights')
ax.set_xlabel('I was aware that I was dreaming.')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

ax.legend(handles=myplt.dlqpatches,loc='upper right',
          title='I was aware that I was dreaming.',
          frameon=False)

plt.tight_layout()
plt.savefig(outfname)
plt.savefig(outfname.replace('.png','.svg'))
plt.close()

