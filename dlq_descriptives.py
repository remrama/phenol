"""
Get summary statistics for the entire DLQ.

Corresponds to figure S1.

Draw boxplots for the DLQ (on with all dreams,
    other with just nonzero lucidity dreams).
Construct descriptives table with means/medians/etc.

Generate plot and table simultaneously, since the plot uses raw data anyways.
"""
from os import path
from json import load
import pandas as pd

import matplotlib.pyplot as plt; plt.ion()
import pyplotparams as myplt


###########  parameter setup  ###########

with open('./config.json') as f:
    p = load(f)
    DATA_DIR  = path.expanduser(p['data_directory'])
    DERIV_DIR = path.expanduser(p['derivatives_directory'])
    DLQ_STRINGS = p['DLQ_probes']
    FLOAT_FMT = p['float_formatting']

DATA_FNAME = path.join(DATA_DIR,'data.csv')

PLOT_FNAME  = path.join(DERIV_DIR,'dlq.eps')
TABLE_FNAME = path.join(DERIV_DIR,'dlq.csv')

FIGURE_WIDTH = 6
FIGURE_HEIGHT_PER_PROBE = .25

BOX_ARGS = {
    'widths'       : .4,
    'vert'         : False,
    'patch_artist' : True,
    'showbox'      : True,
    'showfliers'   : True,
    'showmeans'    : True,
    'meanline'     : True,
    'boxprops'     : dict(facecolor='gainsboro'),
    'medianprops'  : dict(color='red',linewidth=2),
    'meanprops'    : dict(color='black',linewidth=1,linestyle='solid'),
    'flierprops'   : dict(markersize=3),
}

###########################################


###########  load data  ###########

df = pd.read_csv(DATA_FNAME)

# get rid of dreams without recall
df.dropna(subset=['dream_report'],axis=0,inplace=True)

# extract data for plot, which is only the DLQ/MUSK columns
probe_cols = [ col for col in df.columns if 'DLQ' in col or 'MUSK' in col ]
plot_data_all = df[probe_cols].values
plot_data_lim = df.loc[df['DLQ_01']>0,probe_cols].values

###########################################


###########  draw plot  ###########


height = FIGURE_HEIGHT_PER_PROBE * len(probe_cols)
fig, axes = plt.subplots(1,2,figsize=(FIGURE_WIDTH,height))

# loop over two datasets
# (first is all dreams, second is just nonzero-lucidity dreams)
for i, (ax,data) in enumerate(zip(axes,[plot_data_all,plot_data_lim])):
   
    # boxplot
    ax.boxplot(data,**BOX_ARGS)

    # aesthetics
    ax.set_xticks(range(5))
    ax.grid(True,axis='x',which='major',linestyle='--',
            linewidth=.25,color='k',alpha=1)
    if i==0:
        ax.set_title('All dream reports\n')
        yticklabels = [ f'{x} ({i+1:02d})' for i, x in enumerate(DLQ_STRINGS) ]
        ax.set_yticklabels(yticklabels,rotation=0)
        ax.set_xticklabels(list(myplt.DLQ_STRINGS.values()),rotation=25,ha='right')
    elif i==1:
        ax.set_title('Dream reports\nwith nonzero lucidity')
        ax.set_yticklabels([])
        ax.set_xticklabels([])
    ax.invert_yaxis() # flip so DLQ1 is on top
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

# save plot
plt.tight_layout()
plt.savefig(PLOT_FNAME)
plt.close()

###########################################


#######  descriptives table/dataframe  #######

# go from wide to long format
df_melt = df.melt(value_vars=probe_cols,
                  id_vars=['participant_id'],
                  var_name='probe',
                  value_name='likert')

# get mean and quartiles (includes median)
summ_df = df_melt.groupby('probe')['likert'].describe()

# convert to categorical so 0s will show up in crosstab
df_melt['likert'] = pd.Categorical(df_melt['likert'],
                                   categories=range(5),
                                   ordered=True)

# make the contingency table
cont_df = pd.crosstab(df_melt['probe'],
                      df_melt['likert'],
                      dropna=False)

# drop extra layer for column index
cont_df.columns = [ f'freq_likert-{x}' for x in cont_df.columns ]

# combine both dataframes
descr_df = summ_df.join(cont_df)

# save
descr_df.to_csv(TABLE_FNAME,index=True,float_format=FLOAT_FMT)

###########################################
