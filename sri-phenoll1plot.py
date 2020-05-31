"""
Focus on morning mood correlations.

There is more manual here than I'm usually comfortable with
but I'm sure this is a one-time use plot so whateva.
"""
import json

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.patches as mpatches
import matplotlib.patheffects as mpatheffects
import seaborn as sea

import pyplotparams as myplt

from matplotlib import rcParams
rcParams['savefig.dpi'] = 300
rcParams['interactive'] = True
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = 'Arial'
rcParams['axes.spines.top'] = False
rcParams['axes.spines.right'] = False

EXPORT_FNAME = '../results/sri-phenoll1_plot.png'

# load parameters from configuration file
with open('./config.json','r') as f:
    p = json.load(f)
    pos_probes = p['PANAS_positive_probes']
    neg_probes = p['PANAS_negative_probes']
    control_probes = p['DLQ_control_probes']

data_fname = '../data/data.tsv'
resample_fname = '../results/correlations-data.tsv'
stats_fname = '../results/correlations-stats.tsv'

datadf = pd.read_csv(data_fname,sep='\t')
rsmpdf = pd.read_csv(resample_fname,sep='\t',index_col='probe')
statdf = pd.read_csv(stats_fname,sep='\t',index_col='probe')

# manipulate data SAME WAY was done in the correlation script
# generate columns that require manipulations of the raw data
panas_pos_cols = [ f'PANAS_{x:02d}' for x in pos_probes ]
panas_neg_cols = [ f'PANAS_{x:02d}' for x in neg_probes ]
control_cols   = [ f'DLQ_{x:02d}' for x in control_probes ]
datadf['PANAS_pos']     = datadf[panas_pos_cols].sum(axis=1)
datadf['PANAS_neg']     = datadf[panas_neg_cols].sum(axis=1)
datadf['dream_control'] = datadf[control_cols].mean(axis=1)


#######  raw data plots with regression lines  #######


VARIABLES = ['PANAS_pos','PANAS_neg']
n_vars = len(VARIABLES)

# YTICKLABELS = ['Not at all','Just a little','Moderately','Pretty much','Very much']
YTICKLABELS = ['Not at all','','','','Very much']

fig, axes = plt.subplots(1,n_vars,figsize=(n_vars*5,5),sharex=True,sharey=False)

for ax, var in zip(axes.flat,VARIABLES):

    xmin, xmax = (0,30)
    xlabel = dict(PANAS_pos='Next-day positive waking mood',
                  PANAS_neg='Next-day negative waking mood'
            )[var]
    
    # # scatterplot
    # if 'CHAR' in var:
    #     plotdf = datadf[ datadf[var] > 0 ]
    # else:
    #     plotdf = datadf
    sea.swarmplot(y='DLQ_01',x=var,data=datadf,
        size=7,linewidth=1,#jitter=.2,
        color='white',orient='h',ax=ax,
        edgecolor='k')

    ax.invert_yaxis()
    ax.set_yticks(range(0,5))
    ax.set_ylim(-.5,4.5)
    ax.set_xticks([xmin,xmax])
    ax.set_xlabel(xlabel)

    ax.xaxis.set(major_locator=mticker.MultipleLocator(30),
                 minor_locator=mticker.MultipleLocator(10))
    ax.set_xlim(xmin-2,xmax+2)

    ax.grid(True,axis='y',which='major',linestyle='-',
                 linewidth=.5,color='lightgray',alpha=1)
    if ax == axes.flat[0]:
        ax.set_ylabel("Lucidity level of dream" + #r"$\bf{Lucidity\ level}$"
                      "\nNot at all $\leftarrow$                         $\\rightarrow$ Very much",
                      labelpad=0)

        # ax.set_yticklabels(YTICKLABELS,rotation=0)
        ax.set_yticklabels([])
        ax.yaxis.set_ticks_position('none') 
    else:
        ax.set_ylabel('')
        ax.set_yticklabels([])
        for tic in ax.yaxis.get_major_ticks():
            # tic.tick2line.set_visible(False)
            tic.tick1On = tic.tick2On = False

    slope, intercept = statdf.loc[var,['slope_mean','intercept_mean']]
    x = np.arange(xmin,xmax+1)
    line = slope*x + intercept
    ax.plot(x,line,color='k',linewidth=3,solid_capstyle='round',alpha=1)

    if var == 'PANAS_pos':
        stats_txt = "*$\it{r}$ = .35" + "\n$\it{p}$ < .05"
    elif var == 'PANAS_neg':
        stats_txt = "$\it{r}$ = .06" + "\n$\it{p}$ = .75"
    ax.text(1,1.05,stats_txt,fontsize=12,ha='right',va='top',transform=ax.transAxes)
    # ax.text(.5,43.3,'*',fontsize=30,va='center',ha='center')

# clear the
plt.tight_layout()
plt.savefig(EXPORT_FNAME)
plt.close()



# ########### plot the fisher zscores ###########

# n_violins = n_axes
# width = 1 * n_violins
# fig, ax = plt.subplots(figsize=(width,5))

# ymin, ymax = -2.2, 2.2

# violin_data = [ rsmpdf.loc[var,'fishz'].values for var in correlated_vars ]
# viols = ax.violinplot(violin_data,positions=range(n_violins),
#                       widths=pd.np.repeat(.5,n_violins),
#                       showextrema=False)
# plt.setp(viols['bodies'],facecolor='gray',edgecolor='white')

# # add error bars of 95% CI
# for x, var in enumerate(correlated_vars):
#     ci = statdf.loc[var,['fishz_cilo','fishz_cihi']].values
#     y = statdf.loc[var,'fishz_mean']
#     yerr = abs( ci.reshape(2,1) - y )
#     ax.errorbar(x,y,yerr,marker='o',color='k',markersize=1,
#                 capsize=1,capthick=0,linewidth=.5)
#     # significance markers
#     ymark = ymax - .2
#     p, pcorr = statdf.loc[var,['pval','pval_corrected']]
#     if p < .05:
#         ax.plot(x,ymark,marker='*',fillstyle='none',color='k',markersize=7)
#     elif p < .1:
#         ax.plot(x,ymark,marker='^',fillstyle='none',color='k',markersize=7)


# ax.axhline(0,linestyle='--',linewidth=.25,color='k')

# ax.set_ylabel('Correlation with DLQ-1\n($\\tau$ $\it{z}$-score)')
# ax.set_ylim(ymin,ymax)
# ax.yaxis.set_major_locator(MultipleLocator(1))
# ax.yaxis.set_minor_locator(MultipleLocator(.25))
# ax.spines['top'].set_visible(False)
# ax.spines['right'].set_visible(False)


# ax.set_xticks(range(n_violins))
# xticklabels = [ xlabel_dict[var] for var in correlated_vars ]
# ax.set_xticklabels(xticklabels,rotation=33,ha='right')
# ax.set_xlim(-.5,n_violins-.5)

# plt.tight_layout()
# plot_fname = path.join(resdir,'correlations-plot_rs.svg')
# plt.savefig(plot_fname)
# plt.close()
