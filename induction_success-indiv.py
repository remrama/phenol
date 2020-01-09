"""
Plot a single bar per participant.
Each bar shows cumulative counts for
each level of lucidity reported.
"""

from os import path
from json import load
import pandas as pd

import matplotlib; matplotlib.use('Qt5Agg') # python3 bug
import matplotlib.pyplot as plt; plt.ion()

import pyplotparams as myplt


# load parameters from configuration file
with open('./config.json') as f:
    p = load(f)
    resdir  = path.expanduser(p['results_directory'])
infname = path.join(resdir,'dlq01-frequencies.tsv')


########  load and manipulate data  #########

df = pd.read_csv(infname,index_col='participant_id',sep='\t')

# run a cumulative sum across response options for plotting
cumsum_cols = pd.np.roll(df.columns.sort_values(ascending=False),-1).tolist()
cumsum_df = df[cumsum_cols].cumsum(axis=1)

df_fname = path.join(resdir,'induction_success_indiv-data.tsv')
cumsum_df.to_csv(df_fname,index=True,sep='\t')


#########  draw the plot  #########

fig, ax = plt.subplots(figsize=(8,5))

xvals = range(cumsum_df.index.size)
for col, series in cumsum_df.iteritems():
    color = myplt.NORECALL_COLOR if col == 'No recall' else myplt.dlqcolor(int(col[-1]))
    zorder = cumsum_cols[::-1].index(col)
    ax.barh(y=xvals,width=series.values,zorder=zorder,color=color,
        edgecolor='k',linewidth=0)
    if col == 'DLQ01_resp-0':
        ax.barh(y=xvals,width=series.values,zorder=10,color='none',
            edgecolor='k',linewidth=1)


ax.set_xticks(range(cumsum_df.max().max()+1))
ax.set_yticks(range(min(xvals),max(xvals)+1))
ax.set_yticklabels(cumsum_df.index.values)
ax.set_xlabel('Number of nights')
ax.set_ylabel('Participant')
ax.invert_yaxis()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

legend_patches = [myplt.norecall_patch] + myplt.dlqpatches
ax.legend(handles=legend_patches,loc='upper right',
          title='I was aware that I was dreaming.',
          frameon=True,bbox_to_anchor=(1.15,1.15))

plt.tight_layout()
plot_fname = path.join(resdir,'induction_success_indiv-plot.svg')
plt.savefig(plot_fname)
plt.close()



# ############# Plot the amount of data per subject

# fig, ax = plt.subplots(figsize=(8,5))

# xvals = range(resdf.index.size)
# xticklabels = resdf.index.values
# yreported = resdf['n_reported'].values
# yrecalled = resdf['n_recalled'].values
# ylucid    = resdf['n_lucid'].values

# ############## plot different ratings of lucidity within each subj

# # import seaborn as sea
# # sea.countplot(x='DLQ:1',data=df)
# # sea.countplot(x='subj',hue='DLQ:1',data=df,palette='Blues')
# # sea.catplot(x='DLQ:1',col='subj',data=df,kind='count',palette='Blues',col_wrap=4)

# subjorder = resdf.index.values
# resporder = [1,2,3,4,5]

# fig, ax = plt.subplots(figsize=(8,2))

# BARWIDTH = .15
# for xmajor, subj in enumerate(subjorder):
#     dlqvals = df.loc[df['subj']==subj,'DLQ:1'].values
#     for dlqresp in resporder:
#         # center is middle position
#         xminor = resporder.index(dlqresp) - 2
#         xminor *= BARWIDTH # scale it
#         count = sum(dlqvals==dlqresp)
#         x = xmajor + xminor
#         ax.bar(x,height=count,width=BARWIDTH,
#             facecolor=getcolor(dlqresp),
#             edgecolor='k',linewidth=.5,zorder=9)

# ax.set_xticks(range(min(xvals),max(xvals)+1,1))
# ax.set_xticklabels(subjorder)
# ax.set_xlabel('Participant')

# from math import floor
# oldylim = ax.get_ylim()
# ymin, ymax = -.1, oldylim[1]
# ax.set_ylim(ymin,ymax)
# ax.set_yticks([0,floor(ymax)])
# ax.set_ylabel('Number of nights')
# ax.spines['top'].set_visible(False)
# ax.spines['right'].set_visible(False)
# ax.spines['bottom'].set_visible(False)

