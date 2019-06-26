"""
Plot the proportion of lucid dreams across
all subjects and sessions, at different
DLQ1 cutoffs/criteria.
"""

from os import path
import pandas as pd

import matplotlib; matplotlib.use('Qt5Agg') # python3 bug
import matplotlib.pyplot as plt; plt.ion()

import pyplotparams as myplt


resdir = path.expanduser('~/IDrive-Sync/proj/phenol/results')
infname = path.join(resdir,'dlq1-frequency.tsv')


########  load and manipulate data  #########

df = pd.read_csv(infname,index_col='subj',sep='\t')

# get the proportion of LDs at each cutoff
cumsum_cols = pd.np.roll(df.columns.sort_values(ascending=False),-1).tolist()
cumsum_df = df[cumsum_cols].cumsum(axis=1)

total_reports = df.values.sum()
total_drm_reports = df.iloc[:,1:].values.sum()

# don't use response of 1 ("Not at all") or "No recall"
# flip it for interpretability
DLQ_COLS = [ f'DLQ1_resp-{i}' for i in range(2,6) ]

# get the proportion of all reports/attempts
# and also proportion of only times were a dream was recalled
# proportion_lds = [ cumsum_df[col].sum() / total_reports for col in cumsum_df.columns ]
ld_prprtion_of_all  = cumsum_df[DLQ_COLS].apply(lambda srs: srs.sum() / total_reports, axis=0)
ld_prprtion_of_drms = cumsum_df[DLQ_COLS].apply(lambda srs: srs.sum() / total_drm_reports, axis=0)

data = dict(all=ld_prprtion_of_all,recalled=ld_prprtion_of_drms)
markers = dict(all='s',recalled='o')
labels = dict(all='All attempts',recalled='Only recalled dreams')
# append total to the labels
totals = dict(all=total_reports,recalled=total_drm_reports)
for key, lbl in labels.items():
    labels[key] = f'{lbl} ({totals[key]:d})'


#########  draw the plot  #########

fig, ax = plt.subplots(figsize=(5,5))

# draw lines and points separately to have diff colored points
for key, yvals in data.items():
    ax.plot(range(2,6),yvals,
        color='k',linestyle='-',linewidth=1,zorder=1)
    ax.scatter(range(2,6),yvals,
        color=[ myplt.dlqcolor(i) for i in range(2,6) ],
        marker=markers[key],s=150,zorder=2,edgecolors='w',linewidths=.5)

minor_yticks = pd.np.linspace(0,1,21)
major_yticks = pd.np.linspace(0,1,11)
# label yticks with percentages
# major_yticklabels = [ '{:.0f}'.format(x*100) for x in major_yticks ]
ax.set_yticks(minor_yticks,minor=True)
ax.set_xlim(1.5,5.5)
ax.set_ylim(0,1)
ax.set_yticks(major_yticks)
# ax.set_yticklabels(major_yticklabels)
ax.set_xticks(range(2,6))
xticklabels = [ myplt.DLQ_STRINGS[i] for i in range(2,6) ]
xticklabels = [ x if x == 'Very much' else f'>= {x}'
                for x in xticklabels ]
ax.set_xticklabels(xticklabels,rotation=25)
ax.set_ylabel('Proportion of lucid dreams')
ax.set_xlabel('Lucid dream criterion')
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
          title='Data included',
          frameon=True,framealpha=1,edgecolor='k')


plt.tight_layout()

for ext in ['.png','.svg','.eps']:
    plt.savefig(infname.replace('.tsv',f'-proportions{ext}'))
plt.close()
