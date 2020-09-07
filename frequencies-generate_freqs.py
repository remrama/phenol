"""
Generate a frequency table that counts the number of
lucidity level (DLQ1) selected for each participant.

Exports csv table that gets imported
by all the other <frequencies-*> scripts.
"""
from os import path
from json import load
import pandas as pd

## parameters

with open('./config.json') as f:
    p = load(f)
    DATA_DIR  = path.expanduser(p['data_directory'])
    DERIV_DIR = path.expanduser(p['derivatives_directory'])

IMPORT_FNAME = path.join(DATA_DIR,'data.csv')
EXPORT_FNAME = path.join(DERIV_DIR,'ld_freqs.csv')

##

# load data
df_in = pd.read_csv(IMPORT_FNAME)

# get lucidity/DLQ1 frequencies grouped by participant
df_out = df_in.groupby('participant_id')['DLQ_01'
    ].value_counts(dropna=False
    ).unstack(fill_value=0)

# make column names readable
df_out.columns = [ 'No recall' if pd.isna(x) else f'DLQ01_resp-{x:.0f}'
    for x in df_out.columns ]

assert df_out.shape[1] == 6, 'Not all resp options present'

# save
df_out.to_csv(EXPORT_FNAME,index=True)