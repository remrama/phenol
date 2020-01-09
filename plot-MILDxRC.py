"""
Try to visualize relationship between
MILD, reality checks, and lucidity level.
"""
from os import path
import pandas as pd

import matplotlib; matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt; plt.ion()

import pyplotparams as myplt

datadir = path.expanduser('~/IDrive-Sync/proj/phenol/data')
resdir  = path.expanduser('~/IDrive-Sync/proj/phenol/results')

infname = path.join(datadir,'data-clean.tsv')
outfname = path.join(resdir,'results-MILDxRC.svg')

df = pd.read_csv(infname,sep='\t')

DODGE = .05
cmax = df['n_rcs'].max()
cmin = df['n_rcs'].min()
cmap = plt.cm.get_cmap('viridis')

rc_median = df['n_rcs'].median()


fig, ax = plt.subplots(figsize=(7,6))

for dlqresp, respdf in df.groupby('DLQ:1'):

    xvals = respdf['DLQ:1'].values
    yseries = respdf['mildlength']
    colors = respdf['n_rcs'].values
    # colors = [ cmin if x<rc_median else cmax for x in colors ]

    # must dodge overlapping points
    for i, val in enumerate(yseries):
        # check if there are duplicates
        val_idx = yseries.between(val-.5,val+.5,inclusive=True).values
        n_dups = val_idx.sum()
        if n_dups > 1:
            # find where the values are
            duplicate_locs = val_idx.argsort()[-n_dups:]
            # jitter xvalues accordingly
            jitter_vals = pd.np.linspace(-DODGE,DODGE,n_dups)
            xvals[duplicate_locs] += jitter_vals

    sc = ax.scatter(x=yseries.values,y=xvals,c=colors,
                    s=80,cmap=cmap,vmin=cmin,vmax=cmax,
                    marker='o',linewidths=.5,edgecolors='k',zorder=10)


# aesthetics
ax.set_yticks([1,2,3,4,5])
ax.set_xticks([0,5,10,15,20])
ax.set_xticks(range(1,20),minor=True)
ax.set_xlabel('MILD length (minutes)')
ax.set_ylabel('I was aware that I was dreaming')
ax.set_yticklabels(list(myplt.DLQ_STRINGS.values()),rotation=60)
ax.grid(True,axis='y',which='major',linestyle='--',
        linewidth=.25,color='k',alpha=1)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

cbar = plt.colorbar(sc,ticks=[cmin,cmax])
cbar.set_label('Number of reality checks during day')


plt.tight_layout()
plt.savefig(outfname)
plt.close()
