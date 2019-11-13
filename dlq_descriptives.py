"""
Draw boxplots for each DLQ question.
Across all subjects.

For each DLQ probe, plot a box including
data from all attempts that include recall,
and also a box including only responses
that include non-zero awareness.

Also save out descriptives dataframe.
"""
from os import path
from json import load
import pandas as pd

import matplotlib; matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt; plt.ion()

import pyplotparams as myplt


# load directory info from configuration file
with open('./config.json') as f:
    p = load(f)
    DATADIR = path.expanduser(p['data_directory'])
    RESDIR  = path.expanduser(p['results_directory'])
# choose which DLQ probes get plotted
DLQ_COLS = [ f'DLQ:{i}' for i in range(1,20) ]


# load data
infname = path.join(DATADIR,'data-clean.tsv')
df = pd.read_csv(infname,sep='\t')

# get rid of dreams without recall
df.dropna(inplace=True)

# extract data for plot, which is just desired DLQ probes
plot_data_all = df[DLQ_COLS].values
plot_data_lim = df.loc[df['DLQ:1']>1,DLQ_COLS].values

# open figure
fig, axes = plt.subplots(2,1,figsize=(1*len(DLQ_COLS),12))

# loop over two datasets
for i, (ax,data) in enumerate(zip(axes,[plot_data_all,plot_data_lim])):
   
    # boxplot
    ax.boxplot(data,widths=.4,#positions=pd.np.arange(.5,10.5),
               patch_artist=True,showbox=True,showfliers=True,
               boxprops={'facecolor':'gainsboro'},
               medianprops={'color':'red'})

    # aesthetics
    ax.set_yticks([1,2,3,4,5])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(True,axis='y',which='major',linestyle='--',
            linewidth=.25,color='k',alpha=1)
    if i==0:
        ax.set_title('Across all dream reports')
        ax.set_yticklabels(list(myplt.DLQ_STRINGS.values()),rotation=25)
        ax.set_xticklabels([])
    elif i==1:
        ax.set_title('Across all dream reports with nonzero lucidity')
        ax.set_xlabel('survey:probe')
        ax.set_xticklabels(DLQ_COLS,rotation=25)
        ax.set_yticklabels([])

plt.tight_layout()


for ext in ['png','svg','eps']:
    plot_fname = path.join(resdir,f'dlq_descriptives-plot.{ext}')
    plt.savefig(plot_fname)
plt.close()



#### descriptives dataframe

DLQ_COLS = [ f'DLQ:{i}' for i in range(1,20) ]

# first get quartiles for each DLQ question
quartile_df = df[DLQ_COLS].quantile(q=[.25,.5,.75]).T
quartile_df.columns = [ f'quantile_{x}' for x in quartile_df.columns ]

### median and CI??

# now get contingency stuff
# go from wide to long format
df = df.melt(value_vars=DLQ_COLS,
             id_vars=['subj'],
             var_name='probe',value_name='likert')

# convert to categorical so 0s will show up in crosstab
df['likert'] = pd.Categorical(df['likert'],categories=range(1,6),ordered=True)

# make the contingency table
cont_df = pd.crosstab(df['probe'],df['likert'],dropna=False)

# drop extra layer for column index
cont_df.columns = [ f'likert-{x}' for x in cont_df.columns ]


## combine both dataframes
descr_df = pd.concat([cont_df,quartile_df],axis='columns',
    ignore_index=False,sort=True)

# pad index values so they get ordered correctly
def zero_padding(x):
    return 'DLQ:{:02d}'.format(int(x.split(':')[1]))
descr_df.index = descr_df.index.map(zero_padding)
descr_df.sort_index(inplace=True)

# export descriptives dataframe
df_fname = path.join(RESDIR,'dlq_descriptives-data.tsv')
descr_df.to_csv(df_fname,index=True,index_label='probe',sep='\t')
