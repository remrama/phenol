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


DREAM_CHR_COLS = ['Sensory','Neg Emo','Neg Body','Neg Mood',
                  'Bizarreness',' Pos Emo','Pos Body','Pos Mood']


# # to do with catplot instead (all axes at once)
# melted_df = datadf.melt(value_vars=DREAM_CHR_COLS,
#                         id_vars=['subj','DLQ:1'],var_name='dream_chr')
# sea.catplot(y='DLQ:1',x='value',col='dream_chr',data=melted_df,col_wrap=4,
#         height=4,aspect=.75,linewidth=1,#jitter=.2,
#         palette=palette,col_order=DREAM_CHR_COLS,
#         kind='swarm',orient='h')


palette = { x: myplt.dlqcolor(x) for x in myplt.DLQ_STRINGS.keys() }

n_axrows = 2
n_axcols = 4

fig, axes = plt.subplots(n_axrows,n_axcols,figsize=(14,7),
                         squeeze=False,sharex=False,sharey=False)

for ax, var in zip(axes.flat,DREAM_CHR_COLS):

    # scatterplot
    sea.swarmplot(y='DLQ:1',x=var,data=datadf,
        size=6,linewidth=1,#jitter=.2,
        palette=palette,orient='h',ax=ax)

    ax.invert_yaxis()
    ax.set_xlim(.5,10.5)
    ax.set_ylim(-.5,4.5)
    ax.set_xticks(range(1,11))
    ax.set_yticks(range(0,5))
    ax.set_xticklabels([1,'','','','','','','','',10])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    if var == 'Sensory':
        ax.set_ylabel('I was aware that I was dreaming')
        ax.set_yticklabels(list(myplt.DLQ_STRINGS.values()),rotation=25)
    else:
        ax.set_ylabel('')
        ax.set_yticklabels([])
    ax.grid(True,axis='y',which='major',linestyle='--',linewidth=.25,color='k',alpha=1)

    # slope, intercept = resdf.loc[var,['slope','intercept']]
    # x = pd.np.arange(1,11)
    # line = slope*x+intercept
    # ax.plot(x,line,color='k',linewidth=1)

plt.tight_layout()

for ext in ['png','svg','eps']:
    plt.savefig(res_fname.replace('tsv',ext))
plt.close()
