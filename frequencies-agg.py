"""
Lucidity frequncies aggregated across all participants.

Exports 2 histograms, 1 that groups non-zero lucidity and one that doesn't.

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
from matplotlib.ticker import MultipleLocator
import pyplotparams as myplt


########  parameter setup  ########

with open('./config.json') as f:
    p = load(f)
    DERIV_DIR = path.expanduser(p['derivatives_directory'])
    FLOAT_FMT = p['float_formatting']

IMPORT_FNAME = path.join(DERIV_DIR,'ld_freqs.csv')

EXPORT_FNAME_1 = path.join(DERIV_DIR,'ld_freqs-plot.png')
EXPORT_FNAME_2 = path.join(DERIV_DIR,'ld_freqs-plot_nonzero.png')

EXPORT_FNAME_3 = path.join(DERIV_DIR,'ld_freqs-stats.csv')

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
stats_df.to_csv(EXPORT_FNAME_3,float_format=FLOAT_FMT,index=True)

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


##########  draw all frequencies  ###########

fig, ax = plt.subplots(figsize=(4,7))

# for x, y, m in zip(xvals,yvals,markers):
#     c = myplt.dlqcolor(x)
#     ax.scatter(x,y,color=c,marker=m,edgecolors='k',linewidths=.5,s=85)
colors = [ myplt.dlqcolor(i) for i in range(5) ]
xvals = range(5)
ax.bar(xvals,freqs,color=colors,edgecolor='k',width=1,linewidth=.5)

ax.set_xlim(-.75,4.75)
ax.set_ylim(0,max(freqs)+1)
ax.yaxis.set_major_locator(MultipleLocator(20))
ax.yaxis.set_minor_locator(MultipleLocator(5))
ax.set_xticks(range(5))
ax.set_xticklabels(list(myplt.DLQ_STRINGS.values()),rotation=25,ha='right')
ax.set_ylabel('Number of nights')
ax.set_xlabel('I was aware that I was dreaming.')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

ax.legend(handles=myplt.dlqpatches,loc='upper right',
          title='I was aware that I was dreaming.',
          frameon=False)

plt.tight_layout()
plt.savefig(EXPORT_FNAME_1)
plt.close()

####################################


##########  draw just nonlucid vs nonzero_lucid frequencies  ###########

fig, ax = plt.subplots(figsize=(4,7))

colors = [ myplt.dlqcolor(0), 'gray' ]
xvals = [1,2]
yvals = [nonlucid,nonzero_lucid]
ax.bar(xvals,yvals,color=colors,edgecolor='k',width=1,linewidth=.5)

ax.set_xlim(.25,2.75)
ax.set_ylim(0,max(yvals)+1)
ax.yaxis.set_major_locator(MultipleLocator(20))
ax.yaxis.set_minor_locator(MultipleLocator(5))
ax.set_yticklabels([])
ax.set_xticks([1,2])
first_ticklabel = list(myplt.DLQ_STRINGS.values())[0]
second_ticklabel = '>= ' + list(myplt.DLQ_STRINGS.values())[1]
xticklabels = [first_ticklabel,second_ticklabel]
ax.set_xticklabels(xticklabels,rotation=25,ha='right')
ax.set_ylabel('Number of nights')
ax.set_xlabel('I was aware that I was dreaming.')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig(EXPORT_FNAME_2)
plt.close()

####################################
