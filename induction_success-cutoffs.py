"""
Plot the proportion of lucid dreams across
all subjects and sessions, at different
DLQ1 cutoffs/criteria.

Also save data and stats dataframes.

The idea here is not to really get a single
measure of induction success, but to change
the criterion and measure of lucidity to see
how induction success varies as a function
of those two things.
"""
from os import path
from json import load
import pandas as pd
import itertools

from statsmodels.stats.proportion import proportions_ztest
from statsmodels.stats.multitest import fdrcorrection

import matplotlib; matplotlib.use('Qt5Agg') # python3 bug
import matplotlib.pyplot as plt; plt.ion()

import pyplotparams as myplt
from matplotlib.ticker import MultipleLocator



########  load and manipulate data  #########
with open('./config.json') as f:
    p = load(f)
    resdir  = path.expanduser(p['results_directory'])
    FMT = p['float_formatting']
infname = path.join(resdir,'dlq01-frequencies.tsv')

data = pd.read_csv(infname,index_col='participant_id',sep='\t')

n_reports = data.values.sum() # total number of reports
n_dreams = data.iloc[:,1:].values.sum() # all reports that include dream recall
n_subjs = data.shape[0]

# make a dataframe that has both count and proportion
# for lucidity success based on different criterion.
# note that this is a cumulative sum thing.

# get the cumulative sum of LDs at each cutoff
cumsum_cols = pd.np.roll(data.columns.sort_values(ascending=False),-1).tolist()
cumsum_df = data[cumsum_cols].cumsum(axis=1)

# don't use response of 1 ("Not at all") or "No recall"
# flip it for interpretability
DLQ_COLS = [ f'DLQ01_resp-{i}' for i in range(1,5) ]

index = pd.Index(DLQ_COLS,name='cutoff')
columns = ['dreams_past_cutoff','subjs_past_cutoff']

df = pd.DataFrame(columns=columns,index=index)

df['dreams_past_cutoff'] = cumsum_df[DLQ_COLS].sum(axis=0)
df['subjs_past_cutoff']  = cumsum_df[DLQ_COLS].astype(bool).sum(axis=0)

totals = dict(reports=n_reports,dreams=n_dreams,subjs=n_subjs)

df['proportion_reports'] = df['dreams_past_cutoff'] / n_reports
df['proportion_dreams'] = df['dreams_past_cutoff'] / n_dreams
df['proportion_subjs'] = df['subjs_past_cutoff'] / n_subjs

for col in df.columns:
    if 'proportion' in col:
        df[col] = df[col].round(2)


#########  stats  #########

# build the combinations of evals and cutoffs for 2way tests
EVALS = ['subjs','dreams','reports']
CUTOFFS = [1,2,3,4] # nonzero DLQ1 likert responses
cutoff_combos = itertools.combinations(CUTOFFS,2)
eval_cutoff_combos = itertools.product(EVALS,cutoff_combos)
eval_cutoff_combos = [ (x[0],x[1][0],x[1][1])
                      for x in eval_cutoff_combos ]
all_combos = [ (f'eval-{e}_resp-{a}',f'eval-{e}_resp-{b}')
               for e, a, b in eval_cutoff_combos ]
# add comparisons within each cutoff criterion
# 3 comparisons within each
eval_combos = list(itertools.combinations(EVALS,2))
for c in CUTOFFS:
    for a, b in eval_combos:
        all_combos.append( (f'eval-{a}_resp-{c}',f'eval-{b}_resp-{c}') )

# run comparisons
columns = ['z','p']
index = pd.MultiIndex.from_tuples(all_combos,names=['proportion_a','proportion_b'])
stats_df = pd.DataFrame(columns=columns,index=index)

for conda, condb in stats_df.index:
    eva, ca = [ x.split('-')[1] for x in conda.split('_') ]
    evb, cb = [ x.split('-')[1] for x in condb.split('_') ]
    indxa = f'DLQ01_resp-{ca}'
    indxb = f'DLQ01_resp-{cb}'
    col_keya = 'dreams' if eva == 'reports' else eva
    col_keyb = 'dreams' if evb == 'reports' else evb
    cola = f'{col_keya}_past_cutoff'
    colb = f'{col_keyb}_past_cutoff'
    freqa = df.loc[indxa,cola]
    freqb = df.loc[indxb,colb]
    nobs_a = totals[col_keya]
    nobs_b = totals[col_keyb]
    freqs = [freqa,freqb]
    n_obs = [nobs_a,nobs_b]
    z, p = proportions_ztest(freqs,n_obs)
    stats_df.loc[ (conda,condb), ['z','p'] ] = z, p

pvals = stats_df['p']
_, p_corr = fdrcorrection(pvals,method='indep',is_sorted=False)
stats_df['p_corr'] = p_corr

# export data and results dataframes
# round values while also changing output format to print full values
for col in ['z','p','p_corr']:
    stats_df[col] = stats_df[col].map(lambda x: FMT % x)
df_fname = path.join(resdir,'induction_success_cutoffs-data.tsv')
stats_fname = path.join(resdir,'induction_success_cutoffs-stats.tsv')
df.to_csv(df_fname,index=True,sep='\t')
stats_df.to_csv(stats_fname,float_format=FMT,index=True,sep='\t')



#########  draw plot  #########

markers = dict(reports='s',dreams='o',subjs='^')
labels = dict(reports=f'Proportion of all reports ($\mathit{{n}}$={n_reports})',
              dreams=f'Proportion of recalled dreams ($\mathit{{n}}$={n_dreams})',
              subjs=f'Proportion of subjects ($\mathit{{n}}$={n_subjs})')

fig, ax = plt.subplots(figsize=(5,5))

# draw lines and points separately to have diff colored points
for col in df.columns:
    if 'proportion' in col:
        key = col.split('_')[1]
        yvals = df[col].values
        ax.plot(range(1,5),yvals,
            color='k',linestyle='-',linewidth=1,zorder=1)
        ax.scatter(range(1,5),yvals,
            color=[ myplt.dlqcolor(i) for i in range(1,5) ],
            marker=markers[key],edgecolors='w',
            s=150,zorder=2,linewidths=.5)

# handle the xaxis
ax.set_xticks(range(1,5))
xticklabels = [ myplt.DLQ_STRINGS[i] for i in range(1,5) ]
xticklabels = [ x if x == 'Very much' else f'>= {x}'
                for x in xticklabels ]
ax.set_xticklabels(xticklabels,rotation=25,ha='right')
ax.set_xlabel('Lucid dream criterion')

# handle yaxes
ax.yaxis.set_major_locator(MultipleLocator(.1))
ax.yaxis.set_minor_locator(MultipleLocator(.05))
ax.set_xlim(0.5,4.5)
ax.set_ylim(0,1)
ax.set_ylabel('Lucidity induction success')
# ax.set_yticklabels(major_yticklabels)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

ax.grid(True,axis='y',which='minor',
        linestyle='--',linewidth=.25,color='k',alpha=1)

# legend for markers
legend_patches = [ matplotlib.lines.Line2D([],[],
                    label=label,marker=markers[key],
                    color='gray',linestyle='none')
                for key, label in labels.items() ]
ax.legend(handles=legend_patches,loc='upper right',
          title='Evaluation',frameon=True,framealpha=1,edgecolor='k')

plt.tight_layout()

for ext in ['png','svg','eps']:
    plot_fname = path.join(resdir,f'induction_success_cutoffs-plot.{ext}')
    plt.savefig(plot_fname)
plt.close()
