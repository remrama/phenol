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



##########  stats on the frequencies  ###########

# Use chi2 to test the difference among a group
# of proportions, and then pairwise with binomial test.

# is there a difference among the whole DLQ score?
chisq, p = stats.chisquare(yvals)
print('Chi squared stat comparing the frequencies of each DLQ-1 response option',
     f'chisq={chisq:.2f}',f'p={p:.4f}')

# is there a difference among the lucidity options (non-zero)?
nonzero_opts = yvals[1:]
chisq, p = stats.chisquare(nonzero_opts)
print('Chi squared stat comparing the frequencies of non-zero DLQ-1 response options',
     f'chisq={chisq:.2f}',f'p={p:.4f}')

# compare if half the nights had LDs or not**
# but note that we don't really care about this,
# since we also highlight how it depends on how
# you measure success. But run this just to be able
# to say there were about half LDs
obs = [ yvals[0], sum(nonzero_opts) ]
p = stats.binom_test(obs,n=None,p=0.5,alternative='two-sided')
print('Binomial test comparing if half of dreams had some level of lucidity',
     f'p={p:.4f}')
