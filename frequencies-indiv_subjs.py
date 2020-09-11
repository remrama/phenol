"""
Plot a single bar per participant.
Each bar shows cumulative counts for each level of lucidity reported.

Exports figure 1A.

Export the plot and data/counts used to generate the plot.
"""
from os import path
from json import load

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt; plt.ion()
import pyplotparams as myplt


########  load parameters  #########

with open('./config.json') as f:
    p = load(f)
    DERIV_DIR = path.expanduser(p['derivatives_directory'])

IMPORT_FNAME = path.join(DERIV_DIR,'ld_freqs.csv')

EXPORT_FNAME_DATA = path.join(DERIV_DIR,'ld_freqs-subjs.csv')
EXPORT_FNAME_PLOT = path.join(DERIV_DIR,'ld_freqs-subjs.svg')

FIG_WIDTH = 5
FIG_HEIGHT = 3

#############################################


########  load and manipulate data  #########

df = pd.read_csv(IMPORT_FNAME,index_col='participant_id')

# run a cumulative sum across response options for plotting
cumsum_cols = np.roll(df.columns.sort_values(ascending=False),-1).tolist()
cumsum_df = df[cumsum_cols].cumsum(axis=1)

# save
cumsum_df.to_csv(EXPORT_FNAME_DATA,index=True)

#############################################


#########  draw the plot  #########

fig, ax = plt.subplots(figsize=(FIG_WIDTH,FIG_HEIGHT))

xvals = range(cumsum_df.index.size)
for col, series in cumsum_df.iteritems():
    color = myplt.NORECALL_COLOR if col == 'No recall' else myplt.dlqcolor(int(col[-1]))
    zorder = cumsum_cols[::-1].index(col)
    ax.barh(y=xvals,width=series.values,zorder=zorder,color=color,
        edgecolor='k',linewidth=0)
    if col == 'DLQ01_resp-0':
        ax.barh(y=xvals,width=series.values,zorder=10,color='none',
            edgecolor='k',linewidth=1)


ax.set_xticks(range(cumsum_df.max().max()+1))
ax.set_yticks(range(min(xvals),max(xvals)+1))
ax.set_yticklabels(np.arange(cumsum_df.index.nunique())+1)
ax.set_xlabel('Number of nights')
ax.set_ylabel('Participant')
ax.invert_yaxis()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

legend_patches = [myplt.norecall_patch] + myplt.dlqpatches
leg = ax.legend(handles=legend_patches,loc='center left',
                title='       I was aware\nthat I was dreaming.\n          (lucidity)',
                frameon=True,bbox_to_anchor=(1.,.5),
                title_fontsize=10,fontsize=8)
plt.setp(leg.get_title(),fontweight='bold')

plt.tight_layout()
plt.savefig(EXPORT_FNAME_PLOT)
plt.close()

#############################################
