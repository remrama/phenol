"""
Plot DLQ1 by each of the regression model predictors.
Each on its own axis.
"""

from os import path
from json import load
import pandas as pd

import seaborn as sea
import matplotlib.pyplot as plt; plt.ion()
from matplotlib import ticker as mticker

import pyplotparams as myplt


########  parameter setup  ########

with open('./config.json') as f:
    p = load(f)
    DATA_DIR = path.expanduser(p['data_directory'])
    DERIV_DIR = path.expanduser(p['derivatives_directory'])

IMPORT_FNAME = path.join(DATA_DIR,'data.csv')
EXPORT_FNAME = path.join(DERIV_DIR,'adherence.png')

PREDICTORS = ['n_reality_checks','MILD_rehearsal_min','MILD_awake_min']
XLABELS = dict(
    MILD_rehearsal_min='MILD rehearsal\nlength (minutes)',
    n_reality_checks='Number of\nreality checks',
    MILD_awake_min='MILD awake\nlength (minutes)',
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

PALETTE = { x: myplt.dlqcolor(x) for x in myplt.DLQ_STRINGS.keys() }

FIG_HEIGHT = 2
FIG_WIDTH = 1.75*len(PREDICTORS)

###################################


########  draw plot  ########

# load data
df = pd.read_csv(IMPORT_FNAME)

# drop all nights without recall
df.dropna(subset=['dream_report'],axis=0,inplace=True)


fig, axes = plt.subplots(1,len(PREDICTORS),figsize=(FIG_WIDTH,FIG_HEIGHT))


for i, (ax,col) in enumerate(zip(axes,PREDICTORS)):

    sea.swarmplot(y='DLQ_01',x=col,data=df,
        size=4,linewidth=1,#jitter=.2,
        palette=PALETTE,
        ax=ax,orient='h')

    # aesthetics
    ax.set_ylim(-.7,4.7)
    ax.set_yticks([0,1,2,3,4])
    ax.xaxis.set_major_locator(mticker.MultipleLocator(XTICKS_MAJOR[col]))
    ax.xaxis.set_minor_locator(mticker.MultipleLocator(XTICKS_MINOR[col]))
    ax.set_xlabel(XLABELS[col])
    ax.grid(True,axis='y',which='major',linestyle='--',
            linewidth=.25,color='k',alpha=1)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    # ax.invert_yaxis()
    if i==0:
        ax.set_ylabel('Lucidity')
        ax.set_yticklabels(list(myplt.DLQ_STRINGS.values()),rotation=33)
    else:
        ax.set_ylabel('')
        ax.set_yticklabels([])


plt.tight_layout()
plt.savefig(EXPORT_FNAME)
plt.close()

###################################
