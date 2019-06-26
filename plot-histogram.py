"""
Plot a single histogram counting responses
per lucidity level across all participants.
"""

from os import path
import pandas as pd

import matplotlib; matplotlib.use('Qt5Agg') # python3 bug
import matplotlib.pyplot as plt; plt.ion()

import pyplotparams as myplt

resdir = path.expanduser('~/IDrive-Sync/proj/phenol/results')
infname = path.join(resdir,'dlq1-frequency.tsv')


########  load and manipulate data  ########

df = pd.read_csv(infname,sep='\t')




# all_markers = list(matplotlib.markers.MarkerStyle.filled_markers)
# subjs = df['subj'].tolist()
# xvals = []
# yvals = []
# markers = []
# counts = { x: 1 for x in [1,2,3,4,5] }
# for _, row in df.iterrows():
#     resp = row['DLQ:1']
#     if not pd.np.isnan(resp):
#         subj = row['subj']
#         mark = all_markers[subjs.index(subj)]
#         yval = counts[resp]
#         counts[resp] += 1

#         xvals.append(resp)
#         yvals.append(yval)
#         markers.append(mark)



##########  draw it  ###########

fig, ax = plt.subplots(figsize=(4,7))

# for x, y, m in zip(xvals,yvals,markers):
#     c = myplt.dlqcolor(x)
#     ax.scatter(x,y,color=c,marker=m,edgecolors='k',linewidths=.5,s=85)
DLQ_COLS = [ f'DLQ1_resp-{i}' for i in range(1,6) ]
colors = [ myplt.dlqcolor(i) for i in range(1,6) ]
xvals = range(1,6)
yvals = df[DLQ_COLS].sum(axis=0).values
ax.bar(xvals,yvals,color=colors,edgecolor='k',width=1,linewidth=.5)

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

for ext in ['png','svg','eps']:
    plt.savefig(infname.replace('tsv',ext))
plt.close()

