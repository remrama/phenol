"""
Plot the ordinal regression model output for MILD length.
"""
from os import path
from json import load
import pandas as pd

import matplotlib.pyplot as plt; plt.ion()
from matplotlib import ticker as mticker

import pyplotparams as myplt


#########  parameter setup  #########

with open('./config.json') as f:
    p = load(f)
    DERIV_DIR = path.expanduser(p['derivatives_directory'])

IMPORT_FNAME = path.join(DERIV_DIR,'adherence-probs.csv')
EXPORT_FNAME = IMPORT_FNAME.replace('.csv','.svg')

FIG_WIDTH = 2.5
FIG_HEIGHT = 2.5

######################################


#########  load data  #########

df = pd.read_csv(IMPORT_FNAME,index_col='MILD_rehearsal_min')

# run a cumulative sum across response options for plotting
# cumsum_cols = df.columns.sort_values(ascending=False).tolist()
assert all(df.columns.sort_values() == df.columns)
cumsum_df = df.cumsum(axis=1)

###############################


#########  draw plot  #########

xvals = cumsum_df.index.values

fig, ax = plt.subplots(figsize=(FIG_WIDTH,FIG_HEIGHT))

for col, series in cumsum_df.iteritems():
    color = myplt.dlqcolor(int(col[-1]))
    zorder = df.columns[::-1].tolist().index(col) - 10
    ax.fill_between(xvals,series.values,color=color,zorder=zorder)

ax.set_xlim(xvals.min(),xvals.max())
ax.set_ylim(0,1)
ax.set_yticks([0,1])
ax.xaxis.set_major_locator(mticker.MultipleLocator(20))
ax.xaxis.set_minor_locator(mticker.MultipleLocator(5))
ax.set_xlabel('MILD rehearsal length (minutes)')
ax.set_ylabel('Probability of lucidity')

leg = ax.legend(handles=myplt.dlqpatches,loc='lower left',
          title='Lucidity',
          frameon=False,
          title_fontsize=9,fontsize=7,
          labelspacing=0.2, # vertical space between the legend entries
          borderaxespad=0,
)
leg._legend_box.align = "left"

plt.tight_layout()
plt.savefig(EXPORT_FNAME)
plt.close()

###############################
