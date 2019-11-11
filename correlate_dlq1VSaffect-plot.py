"""
Plot relationship between DLQ1 and reported dream characteristics.

Outputs 2 plots
    - swarmplots with regression line
    - distribution of fisherz r values
"""

from os import path
import pandas as pd

import matplotlib; matplotlib.use('Qt5Agg') # python3 bug
import matplotlib.pyplot as plt; plt.ion()
import seaborn as sea

import pyplotparams as myplt

datadir  = path.expanduser('~/DBp/proj/phenoll/data')
resdir  = path.expanduser('~/DBp/proj/phenoll/results')

data_fname = path.join(datadir,'data-clean.tsv')
resample_fname = path.join(resdir,'correlate_affect-data.tsv')
stats_fname = path.join(resdir,'correlate_affect-stats.tsv')


datadf = pd.read_csv(data_fname,sep='\t')
rsmpdf = pd.read_csv(resample_fname,sep='\t',index_col='probe')
statdf = pd.read_csv(stats_fname,sep='\t',index_col='probe')


# have to redo this part, which was done to make the correlations.
# not really worth saving a separate dataframe for it bc easy
POS_PANAS = [1,3,5,9,10,12,14,16,17,19]
pos_panas_cols = [ f'Affect:{x}' for x in POS_PANAS ]
NEG_PANAS = [2,4,6,7,8,11,13,15,18,20]
neg_panas_cols = [ f'Affect:{x}' for x in NEG_PANAS ]
datadf['pos_affect'] = datadf[pos_panas_cols].mean(axis=1)
datadf['neg_affect'] = datadf[neg_panas_cols].mean(axis=1)



# # to do with catplot instead (all axes at once)
# melted_df = datadf.melt(value_vars=DREAM_CHR_COLS,
#                         id_vars=['subj','DLQ:1'],var_name='dream_chr')
# sea.catplot(y='DLQ:1',x='value',col='dream_chr',data=melted_df,col_wrap=4,
#         height=4,aspect=.75,linewidth=1,#jitter=.2,
#         palette=palette,col_order=DREAM_CHR_COLS,
#         kind='swarm',orient='h')


palette = { x: myplt.dlqcolor(x) for x in myplt.DLQ_STRINGS.keys() }

n_axrows = 1
n_axcols = statdf.index.size
height = 5 * n_axrows
width = 5 * n_axcols
fig, axes = plt.subplots(n_axrows,n_axcols,figsize=(width,height),
                         squeeze=False,sharex=False,sharey=False)

for ax, var in zip(axes.flat,statdf.index):

    # scatterplot
    sea.swarmplot(y='DLQ:1',x=var,data=datadf,
        size=6,linewidth=1,#jitter=.2,
        palette=palette,orient='h',ax=ax)

    ax.invert_yaxis()
    ax.set_xlim(.5,5.5)
    ax.set_ylim(-.5,4.5)
    ax.set_xticks(range(1,6))
    ax.set_yticks(range(0,5))
    ax.set_xticklabels([1,'','','',5])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    if ax == axes.flat[0]:
        ax.set_ylabel('I was aware that I was dreaming')
        ax.set_yticklabels(list(myplt.DLQ_STRINGS.values()),rotation=25)
    else:
        ax.set_ylabel('')
        ax.set_yticklabels([])
    if var == 'neg_affect':
        ax.set_xlabel('Negative morning affect')
    elif var == 'pos_affect':
        ax.set_xlabel('Positive morning affect')

    ax.grid(True,axis='y',which='major',linestyle='--',linewidth=.25,color='k',alpha=1)

    slope, intercept = statdf.loc[var,['slope_mean','intercept_mean']]
    x = pd.np.arange(1,6)
    line = slope*x + intercept
    ax.plot(x,line,color='k',linewidth=1)

plt.tight_layout()

for ext in ['png','svg','eps']:
    plot_fname = path.join(resdir,f'correlate_affect-plot.{ext}')
    plt.savefig(plot_fname)
plt.close()