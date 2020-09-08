"""
Plot all the correlations with DLQ1.

Outputs 2 plots
    - swarmplots with regression line
    - distribution of fisherz tau values
"""
from os import path
from json import load

import numpy as np
import pandas as pd

import seaborn as sea
import matplotlib.pyplot as plt; plt.ion()
from matplotlib import ticker as mticker

import pyplotparams as myplt


##########  parameter setup  ##########

with open('./config.json') as f:
    p = load(f)
    DATA_DIR  = path.expanduser(p['data_directory'])
    DERIV_DIR = path.expanduser(p['derivatives_directory'])
    POS_PROBES = p['PANAS_positive_probes']
    NEG_PROBES = p['PANAS_negative_probes']
    CONTROL_PROBES = p['DLQ_control_probes']

PALETTE = { x: myplt.dlqcolor(x) for x in myplt.DLQ_STRINGS.keys() }

IMPORT_FNAME_DATA = path.join(DATA_DIR,'data.csv')
IMPORT_FNAME_CORR = path.join(DERIV_DIR,'correlates_withz.csv')
IMPORT_FNAME_STAT = path.join(DERIV_DIR,'correlates-stats.csv')

EXPORT_FNAME_1 = path.join(DERIV_DIR,'correlates-plot.png')
EXPORT_FNAME_2 = path.join(DERIV_DIR,'correlates-plot_zs.png')

XLABEL_DICT = {
    'CHAR_sensory'       : 'Dream sensory vividness',
    'CHAR_bizarreness'   : 'Dream bizarreness',
    'CHAR_neg_emo'       : 'Dream negative emotion',
    'CHAR_neg_body'      : 'Dream negative body',
    'CHAR_neg_mood'      : 'Awakening negative mood',
    'CHAR_pos_emo'       : 'Dream positive emotion',
    'CHAR_pos_body'      : 'Dream positive body',
    'CHAR_pos_mood'      : 'Awakening positive mood',
    'PANAS_pos'          : 'Positive morning affect',
    'PANAS_neg'          : 'Negative morning affect',
    'dream_control'      : 'Dream control',
    'sleep_quality'      : 'Subjective sleep quality'
}

#######################################


##########  load and manipulate dataa  ##########

datadf = pd.read_csv(IMPORT_FNAME_DATA)
rsmpdf = pd.read_csv(IMPORT_FNAME_CORR,index_col='probe')
statdf = pd.read_csv(IMPORT_FNAME_STAT,index_col='probe')

# drop all nights without recall
datadf.dropna(subset=['dream_report'],axis=0,inplace=True)

# manipulate data SAME WAY was done in the correlation script
# generate columns that require manipulations of the raw data
panas_pos_cols = [ f'PANAS_{x:02d}' for x in POS_PROBES ]
panas_neg_cols = [ f'PANAS_{x:02d}' for x in NEG_PROBES ]
control_cols   = [ f'DLQ_{x:02d}' for x in CONTROL_PROBES ]
datadf['PANAS_pos']     = datadf[panas_pos_cols].sum(axis=1)
datadf['PANAS_neg']     = datadf[panas_neg_cols].sum(axis=1)
datadf['dream_control'] = datadf[control_cols].mean(axis=1)

#######################################


#######  raw data plots with regression lines  #######

xlims_dict = {}
for key in XLABEL_DICT.keys():
    if 'CHAR' in key:
        xlim = (1,9)
    elif 'PANAS' in key:
        xlim = (0,30)
    elif key == 'dream_control':
        xlim = (0,4)
    elif key == 'sleep_quality':
        xlim = (1,7)
    xlims_dict[key] = xlim

# extract all the columns/variables that we correlated
correlated_vars = statdf.index
# one subplot/axis for each variables
n_axes = len(correlated_vars)
n_rows = 3
n_cols = int(np.ceil(n_axes/n_rows))
height = 1.8 * n_rows
width = 1.8 * n_cols

fig, axes = plt.subplots(n_rows,n_cols,figsize=(width,height),
                         squeeze=False,sharex=False,sharey=False)

for ax, var in zip(axes.flat,correlated_vars):

    xmin, xmax = xlims_dict[var]
    xlabel = XLABEL_DICT[var]
    
    # scatterplot
    if 'CHAR' in var:
        plotdf = datadf[ datadf[var] > 0 ]
    else:
        plotdf = datadf
    sea.swarmplot(y='DLQ_01',x=var,data=plotdf,
        size=4,linewidth=1,#jitter=.2,
        palette=PALETTE,orient='h',ax=ax)

    ax.invert_yaxis()
    ax.set_yticks(range(0,5))
    ax.set_ylim(-.5,4.5)
    ax.set_xticks([xmin,xmax])
    ax.set_xlabel(xlabel)
    if xmax > 10:
        ax.xaxis.set_minor_locator(mticker.MultipleLocator(5))
        ax.set_xlim(xmin-2,xmax+2)
    else:
        ax.xaxis.set_minor_locator(mticker.MultipleLocator(1))
        ax.set_xlim(xmin-.5,xmax+.5)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(True,axis='y',which='major',linestyle='--',linewidth=.25,color='k',alpha=1)
    if ax == axes.flat[0]:
        ax.set_ylabel('Lucidity')
        ax.set_yticklabels(list(myplt.DLQ_STRINGS.values()),rotation=25)
    else:
        ax.set_ylabel('')
        ax.set_yticklabels([])
        for tic in ax.yaxis.get_major_ticks():
            tic.tick1line.set_visible(False)
            tic.tick2line.set_visible(False)

    slope, intercept = statdf.loc[var,['slope_mean','intercept_mean']]
    x = np.arange(xmin,xmax+1)
    line = slope*x + intercept
    ax.plot(x,line,color='k',linewidth=1)

# clear the last axis if it's empty
if n_axes % 2 != 0:
    ax = axes.flat[-1]
    ax.clear()
    for x in ['left','right','top','bottom']:
        ax.spines[x].set_visible(False)
    ax.set_xticks([]); ax.set_yticks([])

plt.tight_layout()
plt.savefig(EXPORT_FNAME_1)
plt.close()

#######################################


########### plot the fisher zscores ###########

n_violins = n_axes
width = .4 * n_violins
fig, ax = plt.subplots(figsize=(width,3))

ymin, ymax = -2.2, 2.2

violin_data = [ rsmpdf.loc[var,'fishz'].values for var in correlated_vars ]
viols = ax.violinplot(violin_data,positions=range(n_violins),
                      widths=np.repeat(.5,n_violins),
                      showextrema=False)
plt.setp(viols['bodies'],facecolor='gray',edgecolor='white')

# add error bars of 95% CI
for x, var in enumerate(correlated_vars):
    ci = statdf.loc[var,['fishz_cilo','fishz_cihi']].values
    y = statdf.loc[var,'fishz_mean']
    yerr = abs( ci.reshape(2,1) - y )
    ax.errorbar(x,y,yerr,marker='o',color='k',markersize=1,
                capsize=1,capthick=0,linewidth=.5)
    # significance markers
    ymark = ymax - .2
    p, pcorr = statdf.loc[var,['pval','pval_corrected']]
    if p < .05:
        ax.plot(x,ymark,marker='*',fillstyle='none',color='k',markersize=5,mew=.7)
    elif p < .1:
        ax.plot(x,ymark,marker='^',fillstyle='none',color='k',markersize=5,mew=.7)

ax.axhline(0,linestyle='--',linewidth=.25,color='k')

ax.set_ylabel('Correlation with lucidity\n($\\tau$ $\it{z}$-score)')
ax.set_ylim(ymin,ymax)
ax.yaxis.set_major_locator(mticker.MultipleLocator(1))
ax.yaxis.set_minor_locator(mticker.MultipleLocator(.25))
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

ax.set_xticks(range(n_violins))
xticklabels = [ XLABEL_DICT[var] for var in correlated_vars ]
ax.set_xticklabels(xticklabels,rotation=33,ha='right')
ax.set_xlim(-.5,n_violins-.5)

plt.tight_layout()
plt.savefig(EXPORT_FNAME_2)
plt.close()

#######################################
