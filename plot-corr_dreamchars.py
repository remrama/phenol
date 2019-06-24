"""
Plot relationship between DLQ1 and reported dream characteristics.
"""

from os import path
import pandas as pd

import matplotlib; matplotlib.use('Qt5Agg') # python3 bug
import matplotlib.pyplot as plt; plt.ion()
import seaborn as sea

import pyplotparams as myplt

datadir  = path.expanduser('~/IDrive-Sync/proj/phenol/data')
resdir  = path.expanduser('~/IDrive-Sync/proj/phenol/results')

data_fname = path.join(datadir,'data-clean.tsv')
res_fname = path.join(resdir,'resampled_correlations.tsv')


datadf = pd.read_csv(data_fname,sep='\t')
resdf = pd.read_csv(res_fname,sep='\t',index_col='var')

n_axrows = 1
n_axcols = resdf.shape[0]

palette = { x: myplt.dlqcolor(x) for x in myplt.DLQ_STRINGS.keys() }


fig, axes = plt.subplots(n_axrows,n_axcols,figsize=(9,6),
                         squeeze=False,sharex=True,sharey=True)

for ax, var in zip(axes.flat,resdf.index):

    # scatterplot
    sea.swarmplot(y='DLQ:1',x=var,data=datadf,
        size=10,linewidth=1,#jitter=.2,
        palette=palette,
        ax=ax,orient='h')
    ax.invert_yaxis()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    for i in range(5):
        ax.axhline(i,color='k',linestyle='--',linewidth=.3,zorder=-9)

    # slope, intercept = resdf.loc[var,['slope','intercept']]
    # x = pd.np.arange(1,11)
    # line = slope*x+intercept
    # ax.plot(x,line,color='k',linewidth=1)


axes[0,0].set_xlim(.5,10.5)
axes[0,0].set_ylim(-.5,4.5)
axes[0,0].set_xticks(range(1,11))
axes[0,0].set_yticks(range(0,5))
axes[0,0].set_yticklabels(list(myplt.DLQ_STRINGS.values()),rotation=25)
axes[0,0].set_xticklabels([1,'','','','','','','','',10])
axes[0,0].set_ylabel('I was aware that I was dreaming.')
axes[0,1].set_ylabel('')


# ax.legend(handles=myplt.dlqpatches,loc='upper right',
#           title='I was aware that I was dreaming.',
#           frameon=False,bbox_to_anchor=(1.18,1.18))

plt.tight_layout()
for ext in ['png','svg','eps']:
    plt.savefig(res_fname.replace('tsv',ext))
plt.close()
