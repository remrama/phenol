"""
Plot DLQ1 by each of the regression model predictors.
Each on its own axis.
"""

from os import path
from json import load
import pandas as pd

import matplotlib; matplotlib.use('Qt5Agg') # python3 bug
import matplotlib.pyplot as plt; plt.ion()
import seaborn as sea

import pyplotparams as myplt
from matplotlib.ticker import MultipleLocator


with open('./config.json') as f:
    p = load(f)
    datadir = path.expanduser(p['data_directory'])
    resdir  = path.expanduser(p['results_directory'])

infname = path.join(datadir,'data.tsv')
outfname = path.join(resdir,'ldim_adherence-scatter.png')

df = pd.read_csv(infname,sep='\t')

PREDICTORS = ['n_reality_checks','MILD_rehearsal_min','MILD_awake_min']
XLABELS = dict(
    MILD_rehearsal_min='MILD rehearsal length (minutes)',
    n_reality_checks='Number of reality checks',
    MILD_awake_min='MILD awake length (minutes)',
)
XTICKS_MAJOR = dict( # the spacing for MultipleLocator
    MILD_rehearsal_min=5,
    n_reality_checks=5,
    MILD_awake_min=20,
)
XTICKS_MINOR = dict(
    MILD_rehearsal_min=1,
    n_reality_checks=1,
    MILD_awake_min=5,
)

# # only keep rows with recall
# mildlength = df.loc[~df['DLQ:1'].isnull(),'mildlength'].values
# dlqresp    = df.loc[~df['DLQ:1'].isnull(),'DLQ:1'].values

palette = { x: myplt.dlqcolor(x) for x in myplt.DLQ_STRINGS.keys() }

fig, axes = plt.subplots(1,len(PREDICTORS),figsize=(5*len(PREDICTORS),6))

for i, (ax,col) in enumerate(zip(axes,PREDICTORS)):

    sea.swarmplot(y='DLQ_01',x=col,data=df,
        size=8,linewidth=1,#jitter=.2,
        palette=palette,
        ax=ax,orient='h')

    # aesthetics
    ax.set_ylim(-.7,4.7)
    ax.set_yticks([0,1,2,3,4])
    ax.xaxis.set_major_locator(MultipleLocator(XTICKS_MAJOR[col]))
    ax.xaxis.set_minor_locator(MultipleLocator(XTICKS_MINOR[col]))
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



