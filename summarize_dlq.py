"""
Get median and CI for each DLQ question
across all subjects. Do it once for all
attempts, and again for only attempts
with recall.

Also make contingency tables and export
them as tsv files. (for stats in R)
"""
from os import path
import pandas as pd

datadir = path.expanduser('~/IDrive-Sync/proj/phenol/data')
resdir = path.expanduser('~/IDrive-Sync/proj/phenol/results')

infname = path.join(datadir,'data-clean.tsv')
conttable_outfname = path.join(resdir,'dlq-contingency.tsv')
quartile_outfname = path.join(resdir,'dlq-quartiles.tsv')

indf = pd.read_csv(infname,sep='\t')

# get rid of dreams without recall
indf.dropna(inplace=True)


DLQ_COLS = [ f'DLQ:{i}' for i in range(1,20) ]

# first print out median and CI for each DLQ question
quartile_df = indf[DLQ_COLS].quantile(q=[.25,.5,.75]).T
quartile_df.columns = [ f'quantile_{x}' for x in quartile_df.columns ]

# export table with quartile info
quartile_df.to_csv(quartile_outfname,index=True,index_label='probe',sep='\t')


# go from wide to long format
df = indf.melt(value_vars=DLQ_COLS,
               id_vars=['subj'],
               var_name='probe',value_name='likert')

# convert to categorical so 0s will show up in crosstab
df['likert'] = pd.Categorical(df['likert'],categories=range(1,6),ordered=True)

# make the contingency table
outdf = pd.crosstab(df['probe'],df['likert'],dropna=False)

# drop extra layer for column index
outdf.columns = [ f'likert-{x}' for x in outdf.columns ]


# # only keep main DLQ questions
# excl_df = outdf.loc[DLQ_COLS[:12]]
# stats.chi2_contingency(excl_df)

# export contingency table
outdf.to_csv(conttable_outfname,index=True,sep='\t')
