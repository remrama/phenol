"""
Plot MILD length by DLQ1.
"""

from os import path
import pandas as pd

import matplotlib; matplotlib.use('Qt5Agg') # python3 bug
import matplotlib.pyplot as plt; plt.ion()
import seaborn as sea

import pyplotparams as myplt

datadir = path.expanduser('~/IDrive-Sync/proj/phenol/data')
resdir  = path.expanduser('~/IDrive-Sync/proj/phenol/results')

infname = path.join(datadir,'data-clean.tsv')
outfname = path.join(resdir,'results_regression-scatter.png')

df = pd.read_csv(infname,sep='\t')

# # only keep rows with recall
# mildlength = df.loc[~df['DLQ:1'].isnull(),'mildlength'].values
# dlqresp    = df.loc[~df['DLQ:1'].isnull(),'DLQ:1'].values

palette = { x: myplt.dlqcolor(x) for x in myplt.DLQ_STRINGS.keys() }

fig, ax = plt.subplots(figsize=(7,6))

sea.swarmplot(y='DLQ:1',x='mildlength',data=df,
    size=8,linewidth=1,#jitter=.2,
    palette=palette,
    ax=ax,orient='h')
ax.invert_yaxis()

for i in range(5):
    ax.axhline(i,color='k',linestyle='--',linewidth=.3,zorder=-9)
ax.set_ylim(-.7,4.7)
ax.set_yticks([0,1,2,3,4])
ax.set_yticklabels(list(myplt.DLQ_STRINGS.values()),rotation=60)
ax.set_xticks([0,5,10,15,20])
# ax.set_ylim(mildlength.min()-.1,mildlength.max()+.1)
ax.set_xlabel('MILD length (minutes)')#,fontname='Arial')
ax.set_ylabel('I was aware that I was dreaming.')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

ax.legend(handles=myplt.dlqpatches,loc='upper right',
          title='I was aware that I was dreaming.',
          frameon=False,bbox_to_anchor=(1.18,1.18))

plt.tight_layout()
plt.savefig(outfname)
plt.savefig(outfname.replace('.png','.svg'))
plt.close()



# sea.stripplot(x=dlqresp,y=mildlength,
#     linewidth=1,palette=palette,jitter=2,
#     size=10,
#     ax=ax)

# sea.swarmplot(y='mildlength',data=df,hue='DLQ:1',palette=palette)

# ax.scatter(x=resp-1,y=mildlength,edgecolors='k',
#     color=[ getcolor(x) for x in resp ],linewidths=1,
#     s=80)

# # plt.setp(legend.get_title(),fontsize='xx-small')



