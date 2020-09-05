"""
Get summary statistics for the ENTIRE DLQ.

Here, I'll generate the plot and summary dataframe
simultaneously since this is just a quick aside thing.

Figure A1

Draw boxplots for all DLQ probes
and save out the descriptives dataframe.

Exports one figure with two axes:
    - left side includes all data (with recall)
    - right side includes only data from nonzero lucidity
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
    DATA_DIR = path.expanduser(p['data_directory'])
    DERIV_DIR = path.expanduser(p['derivatives_directory'])
    DLQ_STRINGS = p['DLQ_probes']
    FMT = p['float_formatting']


########### export filenames
plot_fname = path.join(DERIV_DIR,'dlq.png')
df_fname   = path.join(DERIV_DIR,'dlq.csv')


###########  load data  ###########

infname = path.join(DATA_DIR,'data.csv')
df = pd.read_csv(infname)

# get rid of dreams without recall
df.dropna(subset=['dream_report'],axis=0,inplace=True)

# extract data for plot, which is only the DLQ/MUSK columns
probe_cols = [ col for col in df.columns if 'DLQ' in col or 'MUSK' in col ]
plot_data_all = df[probe_cols].values
plot_data_lim = df.loc[df['DLQ_01']>0,probe_cols].values



###########  draw plot  ###########

# open figure
width = 12
height = .5*len(probe_cols)
fig, axes = plt.subplots(1,2,figsize=(width,height))

# loop over two datasets
for i, (ax,data) in enumerate(zip(axes,[plot_data_all,plot_data_lim])):
   
    # boxplot
    ax.boxplot(data,widths=.4,vert=False,patch_artist=True,
               showbox=True,showfliers=True,showmeans=True,meanline=True,
               boxprops={'facecolor':'gainsboro'},
               medianprops={'color':'red','linewidth':2},
               meanprops={'color':'blue','linewidth':2,'linestyle':'dotted'})

    # aesthetics
    ax.set_xticks(range(5))
    ax.grid(True,axis='x',which='major',linestyle='--',
            linewidth=.25,color='k',alpha=1)
    if i==0:
        ax.set_title('Across all dream reports')
        # ax.set_yticklabels(DLQ_COLS,rotation=25)
        yticklabels = [ f'{x} ({i+1:02d})' for i, x in enumerate(DLQ_STRINGS) ]
        ax.set_yticklabels(yticklabels,rotation=0)
        ax.set_xticklabels(list(myplt.DLQ_STRINGS.values()),rotation=25,ha='right')
    elif i==1:
        ax.set_title('Across all dream reports with nonzero lucidity')
        ax.set_yticklabels([])
        ax.set_xticklabels([])
    ax.invert_yaxis() # flip so DLQ1 is on top
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

plt.tight_layout()

plt.savefig(plot_fname)
plt.close()



#######  descriptives dataframe  #######

# first get quartiles for each DLQ question
quartile_df = df[probe_cols].quantile(q=[.25,.5,.75]).T
quartile_df.columns = [ f'quantile_{x}' for x in quartile_df.columns ]

### median and CI??

# now get contingency stuff
# go from wide to long format
df_melt = df.melt(value_vars=probe_cols,
                  id_vars=['participant_id'],
                  var_name='probe',value_name='likert')

# convert to categorical so 0s will show up in crosstab
df_melt['likert'] = pd.Categorical(df_melt['likert'],categories=range(5),ordered=True)

# make the contingency table
cont_df = pd.crosstab(df_melt['probe'],df_melt['likert'],dropna=False)

# drop extra layer for column index
cont_df.columns = [ f'freq_likert-{x}' for x in cont_df.columns ]


## combine both dataframes
descr_df = pd.concat([cont_df,quartile_df],axis='columns',
    ignore_index=False,sort=True)


# export descriptives dataframe
for col in descr_df.columns:
    if 'quantile' in col:
        descr_df[col] = descr_df[col].map(lambda x: FMT % x)
descr_df.to_csv(df_fname,index=True,index_label='probe')
