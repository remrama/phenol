"""
Plot all the correlations with DLQ1.

Outputs 2 plots
    - swarmplots with regression line
    - distribution of fisherz r values
"""
from os import path
from json import load
import pandas as pd

import matplotlib; matplotlib.use('Qt5Agg') # python3 bug
import matplotlib.pyplot as plt; plt.ion()
from matplotlib.ticker import MultipleLocator
import seaborn as sea

import pyplotparams as myplt


# load analysis parameters from configuration file
with open('./config.json') as f:
    p = load(f)
    datadir = path.expanduser(p['data_directory'])
    resdir  = path.expanduser(p['results_directory'])
    pos_probes = p['PANAS_positive_probes']
    neg_probes = p['PANAS_negative_probes']
    control_probes = p['DLQ_control_probes']

data_fname = path.join(datadir,'data-clean.tsv')
resample_fname = path.join(resdir,'correlate_dlq1-data.tsv')
stats_fname = path.join(resdir,'correlate_dlq1-stats.tsv')

datadf = pd.read_csv(data_fname,sep='\t')
rsmpdf = pd.read_csv(resample_fname,sep='\t',index_col='probe')
statdf = pd.read_csv(stats_fname,sep='\t',index_col='probe')

# manipulate data SAME WAY was done in the correlation script
# generate columns that require manipulations of the raw data
panas_pos_cols = [ f'Affect:{x}' for x in pos_probes ]
panas_neg_cols = [ f'Affect:{x}' for x in neg_probes ]
control_cols   = [ f'DLQ:{x}' for x in control_probes ]
datadf['panas_pos']     = datadf[panas_pos_cols].mean(axis=1)
datadf['panas_neg']     = datadf[panas_neg_cols].mean(axis=1)
datadf['dream_control'] = datadf[control_cols].mean(axis=1)


# # to do with catplot instead (all axes at once)
# melted_df = datadf.melt(value_vars=DREAM_CHR_COLS,
#                         id_vars=['subj','DLQ:1'],var_name='dream_chr')
# sea.catplot(y='DLQ:1',x='value',col='dream_chr',data=melted_df,col_wrap=4,
#         height=4,aspect=.75,linewidth=1,#jitter=.2,
#         palette=palette,col_order=DREAM_CHR_COLS,
#         kind='swarm',orient='h')


palette = { x: myplt.dlqcolor(x) for x in myplt.DLQ_STRINGS.keys() }

xlabel_dict = {
    'Sensory'       : 'Sensory vividness',
    'Bizarreness'   : 'Bizarreness',
    'Neg Emo'       : 'Negative emotion',
    'Neg Body'      : 'Negative body',
    'Neg Mood'      : 'Negative mood',
    ' Pos Emo'      : 'Positive emotion',
    'Pos Body'      : 'Positive body',
    'Pos Mood'      : 'Positive mood',
    'panas_pos'     : 'Positive morning affect',
    'panas_neg'     : 'Negative morning affect',
    'dream_control' : 'Dream control'
}
# all variables have a minimum of 1, but the max is different
low_xmax_vars = ['panas_pos','panas_neg','dream_control']
xlims_dict = { var: 5 if var in low_xmax_vars else 10
    for var in xlabel_dict.keys() }

# extract all the columns/variables that we correlated
correlated_vars = statdf.index
# one subplot/axis for each variables
n_axes = len(correlated_vars)
n_rows = 2
n_cols = int(pd.np.ceil(11/2))
height = 5 * n_rows
width = 5 * n_cols

fig, axes = plt.subplots(n_rows,n_cols,figsize=(width,height),
                         squeeze=False,sharex=False,sharey=False)

for ax, var in zip(axes.flat,correlated_vars):

    xmax = xlims_dict[var]
    xlabel = xlabel_dict[var]
    
    # scatterplot
    sea.swarmplot(y='DLQ:1',x=var,data=datadf,
        size=6,linewidth=1,#jitter=.2,
        palette=palette,orient='h',ax=ax)

    ax.invert_yaxis()
    ax.set_yticks(range(0,5))
    ax.set_ylim(-.5,4.5)
    ax.set_xlim(.5,xmax+.5)
    ax.set_xticks(range(1,xmax+1))
    xticklabels = [''] * xmax
    # dream control is 0-4 actually
    xticklabels[0] = 1 if var != 'dream_control' else 0
    xticklabels[-1] = xmax if var != 'dream_control' else xmax-1
    ax.set_xticklabels(xticklabels)
    # ax.xaxis.set_major_locator(MultipleLocator(xmax))
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    if ax == axes.flat[0]:
        ax.set_ylabel('I was aware that I was dreaming')
        ax.set_yticklabels(list(myplt.DLQ_STRINGS.values()),rotation=25)
    else:
        ax.set_ylabel('')
        ax.set_yticklabels([])
    ax.set_xlabel(xlabel)

    ax.grid(True,axis='y',which='major',linestyle='--',linewidth=.25,color='k',alpha=1)

    slope, intercept = statdf.loc[var,['slope_mean','intercept_mean']]
    x = pd.np.arange(1,xmax+1)
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
for ext in ['png','svg','eps']:
    plot_fname = path.join(resdir,f'correlate_dlq1-plot.{ext}')
    plt.savefig(plot_fname)
plt.close()



########### plot the fisher zscores ###########

n_violins = n_axes
width = 1 * n_violins
fig, axes = plt.subplots(2,1,figsize=(width,10),
                         sharex=True,sharey=False)

for ax, metric in zip(axes,['r','rfishz']):

    violin_data = [ rsmpdf.loc[var,metric].values for var in correlated_vars ]
    viols = ax.violinplot(violin_data,positions=range(n_violins),
                          widths=pd.np.repeat(.5,n_violins),
                          showextrema=False)
    plt.setp(viols['bodies'],facecolor='gray',edgecolor='white')

    # add error bars of 95% CI
    for x, var in enumerate(correlated_vars):
        ci = statdf.loc[var,[f'{metric}_cilo',f'{metric}_cihi']].values
        y = statdf.loc[var,f'{metric}_mean']
        yerr = abs( ci.reshape(2,1) - y )
        ax.errorbar(x,y,yerr,marker='o',color='k',markersize=1,
                    capsize=1,capthick=0,linewidth=.5)

    ax.axhline(0,linestyle='--',linewidth=.25,color='k')

    if metric == 'r':
        ylabel = 'Correlation with DLQ1 ($\it{r}$)'
        ymin, ymax = -1.1, 1.1
    elif metric == 'rfishz':
        ylabel = 'Correlation with DLQ1\n(Fisher z-transformed $\it{r}$ value)'
        ymin, ymax = -2.2, 2.2
    ax.set_ylabel(ylabel)
    ax.set_ylim(ymin,ymax)
    ax.yaxis.set_major_locator(MultipleLocator(1))
    ax.yaxis.set_minor_locator(MultipleLocator(.25))
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

ax.set_xticks(range(n_violins))
xticklabels = [ xlabel_dict[var] for var in correlated_vars ]
ax.set_xticklabels(xticklabels,rotation=33,ha='right')
ax.set_xlim(-.5,n_violins-.5)

plt.tight_layout()

for ext in ['png','svg','eps']:
    plot_fname = path.join(resdir,f'correlate_dlq1-plot_rs.{ext}')
    plt.savefig(plot_fname)
plt.close()
