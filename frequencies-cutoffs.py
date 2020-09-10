"""
Plot the proportion of lucid dreams across
all subjects and sessions, at different
DLQ1 cutoffs/criteria.

Corresponds to figure 1C.

Also export data and stats performed on data.

The idea here is not to really get a single
measure of induction success, but to change
the criterion and measure of lucidity to see
how induction success varies as a function
of those two things.
"""
from os import path
from json import load
import itertools

import numpy as np
import pandas as pd
import pingouin as pg

import matplotlib.pyplot as plt; plt.ion()
from matplotlib import lines as mlines
from matplotlib import ticker as mticker

import pyplotparams as myplt


########  parameter setup  #########

with open('./config.json') as f:
    p = load(f)
    DERIV_DIR = path.expanduser(p['derivatives_directory'])
    FLOAT_FMT = p['float_formatting']

IMPORT_FNAME = path.join(DERIV_DIR,'ld_freqs.csv')

EXPORT_FNAME_DATA = path.join(DERIV_DIR,'ld_freqs-cutoffs_data.csv')
EXPORT_FNAME_STAT = path.join(DERIV_DIR,'ld_freqs-cutoffs_stats.csv')
EXPORT_FNAME_PLOT = path.join(DERIV_DIR,'ld_freqs-cutoffs_plot.png')

FIG_WIDTH = 3
FIG_HEIGHT = 3

DLQ_COLS = [ f'DLQ01_resp-{i}' for i in range(5) ]
RESP_COLS = [ 'No recall' ] + DLQ_COLS

EVALS = ['ld_per_dream','ld_per_night','binary_ld']
CUTOFFS = [1,2,3,4] # nonzero DLQ1 likert responses

####################################


########  load and manipulate data  #########

df = pd.read_csv(IMPORT_FNAME,index_col='participant_id')

for ev in EVALS:
    for c in CUTOFFS:

        # pick which columns represent a lucid dream
        lucid_cols = DLQ_COLS[c:]

        n_lucids = df[lucid_cols].sum(axis=1)

        new_col = f'{ev}-cutoff_{c}'

        if ev == 'binary_ld':
            df[new_col] = (n_lucids > 0).astype(float)
        elif ev == 'ld_per_dream':
            df[new_col] = (n_lucids / df[DLQ_COLS].sum(axis=1)).fillna(0)
        elif ev == 'ld_per_night':
            df[new_col] = (n_lucids / df[RESP_COLS].sum(axis=1)).fillna(0)


# break into long format and groupby evaluation/cutoff

melted = pd.melt(df.reset_index(),
    value_vars=[ c for c in df.columns if 'cutoff' in c ],
    id_vars='participant_id',
    value_name='ld_rate')

melted['eval'], melted['cutoff'] = zip(*melted['variable'].str.split('-'))
avgs = melted.groupby(['eval','cutoff']
    )['ld_rate'].agg(['mean','sem'])

# replace sem for the binary case bc it's meaningless
avgs.loc['binary_ld','sem'] = pd.NA

anova = pg.rm_anova(data=melted[melted['eval']!='binary_ld'],
    dv='ld_rate',within=['eval','cutoff'],
    subject='participant_id',detailed=True)

avgs.to_csv(EXPORT_FNAME_DATA,float_format=FLOAT_FMT,index=True,na_rep='NA')
anova.to_csv(EXPORT_FNAME_STAT,float_format=FLOAT_FMT,index=False)

####################################


#########  draw plot  #########

markers = dict(ld_per_dream='s',ld_per_night='o',binary_ld='^')
labels = dict(ld_per_night='LDs per night',
              ld_per_dream='LDs per night with recall',
              binary_ld='Binarized rate')

fig, ax = plt.subplots(figsize=(FIG_WIDTH,FIG_HEIGHT))

# draw lines and points separately to have diff colored points
for ev, subdf in avgs.groupby('eval'):

    xvals = np.arange(4).astype(float)
    if ev == 'ld_per_night':
        xvals -= .07
    elif ev == 'ld_per_dream':
        xvals += .07
    yvals = subdf['mean']

    if ev != 'binary_ld':
        yerr  = subdf['sem']
        ax.errorbar(xvals,yvals,yerr,
            color='k',linestyle='-',linewidth=.5,zorder=1)
    else:
        ax.plot(xvals,yvals,
            color='k',linestyle='-',linewidth=.5,zorder=1)
    ax.scatter(xvals,yvals,
        color=[ myplt.dlqcolor(i) for i in range(1,5) ],
        marker=markers[ev],edgecolors='w',
        s=70,zorder=2,linewidths=1)

# handle the xaxis
ax.set_xticks(range(4))
xticklabels = [ myplt.DLQ_STRINGS[i] for i in range(1,5) ]
xticklabels = [ x if x == 'Very much' else f'>= {x}'
                for x in xticklabels ]
ax.set_xticklabels(xticklabels,rotation=25,ha='right')
ax.set_xlabel('Lucidity cutoff')

# handle yaxes
ax.yaxis.set_major_locator(mticker.MultipleLocator(.5))
ax.yaxis.set_minor_locator(mticker.MultipleLocator(.1))
ax.set_xlim(-0.5,3.5)
ax.set_ylim(0,1)
ax.set_ylabel('Lucid dream frequency')
# ax.set_yticklabels(major_yticklabels)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

ax.grid(True,axis='y',which='both',
        linestyle='--',linewidth=.25,color='k',alpha=1)

# legend for markers
legend_patches = [ mlines.Line2D([],[],
                    label=label,marker=markers[key],
                    color='gray',linestyle='none')
                for key, label in labels.items() ]
leg = ax.legend(handles=legend_patches,loc='upper right',
          title='Evaluation',frameon=True,framealpha=1,edgecolor='k',
          handletextpad=-0.2, # space between legend marker and label
          labelspacing=0.2, # like rowspacing, vertical space between the legend entries
          title_fontsize=10,fontsize=8)

plt.tight_layout()
plt.savefig(EXPORT_FNAME_PLOT)
plt.close()

####################################
