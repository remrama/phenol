"""
Plot DLQ1 by each of the regression model predictors.
Each on its own axis.
"""

from os import path
import pandas as pd

import matplotlib; matplotlib.use('Qt5Agg') # python3 bug
import matplotlib.pyplot as plt; plt.ion()
import seaborn as sea

import pyplotparams as myplt

datadir = path.expanduser('~/IDrive-Sync/proj/phenol/data')
resdir  = path.expanduser('~/IDrive-Sync/proj/phenol/results')

infname = path.join(datadir,'data-clean.tsv')
outfname = path.join(resdir,'results_regression-scatter.png')

df = pd.read_csv(infname,sep='\t')

PREDICTORS = ['mildlength','n_rcs','wbtblength','bedtime_int']
XLABELS = dict(
    mildlength='MILD length (minutes)',
    n_rcs='Number of reality checks',
    wbtblength='WBTB length (minutes)',
    bedtime_int='Hours away from midnight',
)
XTICKS_MAJOR = dict(
    mildlength=pd.np.linspace(0,20,5),
    n_rcs=[0,5,10],
    wbtblength=pd.np.linspace(0,60,4),
    bedtime_int=[-10,-5,0,5,10],
)
XTICKS_MINOR = dict(
    mildlength=pd.np.linspace(0,20,21),
    n_rcs=pd.np.linspace(0,13,14),
    wbtblength=pd.np.linspace(0,60,13),
    bedtime_int=pd.np.linspace(-13,13,27),
)

# # only keep rows with recall
# mildlength = df.loc[~df['DLQ:1'].isnull(),'mildlength'].values
# dlqresp    = df.loc[~df['DLQ:1'].isnull(),'DLQ:1'].values

palette = { x: myplt.dlqcolor(x) for x in myplt.DLQ_STRINGS.keys() }

fig, axes = plt.subplots(1,len(PREDICTORS),figsize=(7*len(PREDICTORS),6))

for i, (ax,col) in enumerate(zip(axes,PREDICTORS)):

    sea.swarmplot(y='DLQ:1',x=col,data=df,
        size=8,linewidth=1,#jitter=.2,
        palette=palette,
        ax=ax,orient='h')

    # aesthetics
    ax.set_ylim(-.7,4.7)
    ax.set_yticks([0,1,2,3,4])
    ax.set_xticks(XTICKS_MAJOR[col])
    ax.set_xticks(XTICKS_MINOR[col],minor=True)
    ax.set_xlabel(XLABELS[col])
    ax.grid(True,axis='y',which='major',linestyle='--',
            linewidth=.25,color='k',alpha=1)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    # ax.invert_yaxis()
    if i==0:
        ax.set_ylabel('I was aware that I was dreaming')
        ax.set_yticklabels(list(myplt.DLQ_STRINGS.values()),rotation=60)
    else:
        ax.set_ylabel('')
        ax.set_yticklabels([])

    # ax.set_ylim(mildlength.min()-.1,mildlength.max()+.1)
    if i == len(PREDICTORS)-1:
        ax.legend(handles=myplt.dlqpatches,loc='upper right',
                  title='I was aware that I was dreaming.',
                  frameon=False,bbox_to_anchor=(1.18,1.18))

plt.tight_layout()
plt.savefig(outfname)
plt.savefig(outfname.replace('png','svg'))
plt.savefig(outfname.replace('png','eps'))
plt.close()



# sea.stripplot(x=dlqresp,y=mildlength,
#     linewidth=1,palette=palette,jitter=2,
#     size=10,
#     ax=ax)

# sea.swarmplot(y='mildlength',data=df,hue='DLQ:1',palette=palette)

# ax.scatter(x=resp-1,y=mildlength,edgecolors='k',
#     color=[ getcolor(x) for x in resp ],linewidths=1,
#     s=80)

# # plt.setp(legend.get_title(),fontsize='xx-small')



