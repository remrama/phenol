"""
Lucidity frequncies aggregated across all participants.

Exports 2 histograms, 1 that groups non-zero lucidity and one that doesn't.
But 1 figure, latter is inset of former.

Corresponds to figure 1B.

Also export stats dataframe that runs chisquare
across all DLQs (main plot) and binomial test on subplot.
"""
from os import path
from json import load

import numpy as np
import pandas as pd
from scipy import stats

import matplotlib.pyplot as plt; plt.ion()
from matplotlib import ticker as mticker
import pyplotparams as myplt


########  parameter setup  ########

with open('./config.json') as f:
    p = load(f)
    DERIV_DIR = path.expanduser(p['derivatives_directory'])
    FLOAT_FMT = p['float_formatting']

IMPORT_FNAME = path.join(DERIV_DIR,'ld_freqs.csv')

EXPORT_FNAME_PLOT = path.join(DERIV_DIR,'ld_freqs-plot.png')
EXPORT_FNAME_STAT = path.join(DERIV_DIR,'ld_freqs-stats.csv')

FIG_WIDTH = 1.75
FIG_HEIGHT = 3

TICK_FONTSIZE = 6 # diff than custom defaults
XTICK_FONTSIZE_INSET = 6

####################################


########  load data  ########

df = pd.read_csv(IMPORT_FNAME)

DLQ_COLS = [ f'DLQ01_resp-{i}' for i in range(5) ]
freqs = df[DLQ_COLS].sum(axis=0).values

####################################


##########  stats on the frequencies  ###########

comparisons = ['across_DLQ01','across_nonzeroDLQ01','zeroVSnonzero_DLQ01']
index = pd.Index(comparisons,name='comparison')
stats_df = pd.DataFrame(columns=['test','chisq','pval'],index=index)

# Use chi2 to test the difference among a group
# of proportions, and then pairwise with binomial test.

# is there a difference among the whole DLQ score?
chisq, p = stats.chisquare(freqs)
stats_df.loc['across_DLQ01',['test','chisq','pval']] = ['chisquare',chisq,p]

# is there a difference among the lucidity options (non-zero)?
nonzero_opts = freqs[1:]
chisq, p = stats.chisquare(nonzero_opts)
stats_df.loc['across_nonzeroDLQ01',['test','chisq','pval']] = ['chisquare',chisq,p]

# compare if half the nights had LDs or not**
# but note that we don't really care about this,
# since we also highlight how it depends on how
# you measure success. But run this just to be able
# to say there were about half LDs
nonlucid = freqs[0]
nonzero_lucid = sum(nonzero_opts)
obs = [nonlucid,nonzero_lucid]
p = stats.binom_test(obs,p=0.5,alternative='two-sided')
stats_df.loc['zeroVSnonzero_DLQ01',['test','chisq','pval']] = ['binomial',np.nan,p]

# export stats dataframe
stats_df['chisq'] = stats_df['chisq'].astype(float)
stats_df['pval']  = stats_df['pval'].astype(float)
stats_df.to_csv(EXPORT_FNAME_STAT,float_format=FLOAT_FMT,index=True)

####################################


##########  draw all frequencies  ###########

fig, ax = plt.subplots(figsize=(FIG_WIDTH,FIG_HEIGHT))

colors = [ myplt.dlqcolor(i) for i in range(5) ]
xvals = range(5)
ax.bar(xvals,freqs,color=colors,edgecolor='k',width=1,linewidth=.5)

ax.set_xlim(-.75,4.75)
ax.set_ylim(0,max(freqs)+1)
ax.yaxis.set_major_locator(mticker.MultipleLocator(20))
ax.yaxis.set_minor_locator(mticker.MultipleLocator(5))
ax.set_xticks(range(5))
ax.set_xticklabels(list(myplt.DLQ_STRINGS.values()),rotation=25,
                   ha='right',fontsize=TICK_FONTSIZE)
ax.set_ylabel('Number of nights')
ax.set_xlabel('Lucidity')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

####################################


##########  draw just nonlucid vs nonzero_lucid frequencies  ###########

ax2 = ax.inset_axes([0.6, 0.6, 0.4, 0.5])

colors = [ myplt.dlqcolor(0), 'gray' ]
xvals = [1,2]
yvals = [nonlucid,nonzero_lucid]
ax2.bar(xvals,yvals,color=colors,edgecolor='k',width=1,linewidth=.5)

ax2.set_xlim(.25,2.75)
ax2.set_ylim(0,max(yvals)+1)
ax2.yaxis.set_major_locator(mticker.MultipleLocator(20))
ax2.yaxis.set_minor_locator(mticker.MultipleLocator(5))
ax2.set_yticklabels([])
ax2.set_xticks([1,2])
first_ticklabel = list(myplt.DLQ_STRINGS.values())[0]
second_ticklabel = '>= ' + list(myplt.DLQ_STRINGS.values())[1]
xticklabels = [first_ticklabel,second_ticklabel]
ax2.set_xticklabels(xticklabels,rotation=25,ha='right',fontsize=XTICK_FONTSIZE_INSET)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
for tic in ax2.xaxis.get_major_ticks():
    tic.tick1line.set_visible(False)
    tic.tick2line.set_visible(False)

plt.tight_layout()
plt.savefig(EXPORT_FNAME_PLOT)
plt.close()

####################################
