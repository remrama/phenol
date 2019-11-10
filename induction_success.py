"""
Plot a single histogram counting responses
per lucidity level across all participants.
"""

from os import path
import pandas as pd
from scipy import stats

import matplotlib; matplotlib.use('Qt5Agg') # python3 bug
import matplotlib.pyplot as plt; plt.ion()

import pyplotparams as myplt

resdir = path.expanduser('~/DBp/proj/phenoll/results')
infname = path.join(resdir,'dlq1-frequency.tsv')


########  load and manipulate data  ########

df = pd.read_csv(infname,sep='\t')

DLQ_COLS = [ f'DLQ1_resp-{i}' for i in range(1,6) ]
freqs = df[DLQ_COLS].sum(axis=0).values


##########  stats on the frequencies  ###########

comparisons = ['across_DLQ1','across_nonzeroDLQ1','zeroVSnonzero_DLQ1']
index = pd.Index(comparisons,name='comparison')
stats_df = pd.DataFrame(columns=['test','chisq','pval'],index=index)

# Use chi2 to test the difference among a group
# of proportions, and then pairwise with binomial test.

# is there a difference among the whole DLQ score?
chisq, p = stats.chisquare(freqs)
stats_df.loc['across_DLQ1',['test','chisq','pval']] = ['chisquare',chisq,p]

# is there a difference among the lucidity options (non-zero)?
nonzero_opts = freqs[1:]
chisq, p = stats.chisquare(nonzero_opts)
stats_df.loc['across_nonzeroDLQ1',['test','chisq','pval']] = ['chisquare',chisq,p]

# compare if half the nights had LDs or not**
# but note that we don't really care about this,
# since we also highlight how it depends on how
# you measure success. But run this just to be able
# to say there were about half LDs
obs = [ freqs[0], sum(nonzero_opts) ]
p = stats.binom_test(obs,p=0.5,alternative='two-sided')
stats_df.loc['zeroVSnonzero_DLQ1',['test','chisq','pval']] = ['binomial',pd.np.nan,p]

# round values while also changing output format to print full values
stats_df['chisq'] = stats_df['chisq'].map(lambda x: '%.02f' % x)
stats_df['pval'] = stats_df['pval'].map(lambda x: '%.04f' % x)

# export stats dataframe
stats_fname = path.join(resdir,'induction_success-stats.tsv')
stats_df.to_csv(stats_fname,index=True,sep='\t')

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
colors = [ myplt.dlqcolor(i) for i in range(1,6) ]
xvals = range(1,6)
ax.bar(xvals,freqs,color=colors,edgecolor='k',width=1,linewidth=.5)

ax.set_xlim(.25,5.75)
ax.set_ylim(0,max(freqs)+1)
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
    plot_fname = path.join(resdir,f'induction_success-plot.{ext}')
    plt.savefig(plot_fname)
plt.close()
