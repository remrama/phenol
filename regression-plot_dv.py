"""
Plot the ordinal regression model output for MILD length.
"""

from os import path
from json import load
import pandas as pd

import matplotlib; matplotlib.use('Qt5Agg') # python3 bug
import matplotlib.pyplot as plt; plt.ion()

import pyplotparams as myplt


with open('./config.json') as f:
    p = load(f)
    resdir  = path.expanduser(p['results_directory'])

infname = path.join(resdir,'ldim_adherence-effects.tsv')


#########  load and manipulate data  #########

df = pd.read_csv(infname,sep='\t',index_col='mildlength')

# run a cumulative sum across response options for plotting
# cumsum_cols = df.columns.sort_values(ascending=False).tolist()
assert all(df.columns.sort_values() == df.columns)
cumsum_df = df.cumsum(axis=1)


#########  draw plot  #########

xvals = cumsum_df.index.values

fig, ax = plt.subplots(figsize=(7,6))

for col, series in cumsum_df.iteritems():
    color = myplt.dlqcolor(int(col[-1]))
    zorder = df.columns[::-1].tolist().index(col) - 10
    ax.fill_between(xvals,series.values,color=color,zorder=zorder)


ax.set_xlim(xvals.min(),xvals.max())
ax.set_ylim(0,1)
ax.set_yticks([0,1])
ax.set_xticks([0,5,10,15,20])
ax.set_xlabel('MILD length (minutes)')
ax.set_ylabel('Probability')

ax.legend(handles=myplt.dlqpatches,loc='lower left',
          title='I was aware that I was dreaming.',
          frameon=False)

plt.tight_layout()
for ext in ['png','svg','eps']:
    plt.savefig(infname.replace('tsv',ext))
plt.close()
