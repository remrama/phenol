"""
Generate a frequency table that counts the amount of
lucidity level selections (i.e., DLQ-1) for each participant.

Exports csv table that gets imported
by all the other <frequencies-*> scripts.
"""
from os import path
from json import load

import pandas as pd

with open('./config.json') as f:
    p = load(f)
    DATA_DIR        = path.expanduser(p['data_directory'])
    DERIVATIVES_DIR = path.expanduser(p['derivatives_directory'])

IMPORT_FNAME = path.join(DATA_DIR,'data.csv')
EXPORT_FNAME = path.join(DERIVATIVES_DIR,'ld_freqs.csv')

df_in = pd.read_csv(IMPORT_FNAME)

df_out = df_in.groupby('participant_id')['DLQ_01'
    ].value_counts(dropna=False
    ).unstack(fill_value=0)

df_out.columns = [ 'No recall' if pd.isna(x) else f'DLQ01_resp-{x:.0f}'
    for x in df_out.columns ]

assert df_out.shape[1] == 6, 'Not all resp options present'

df_out.to_csv(EXPORT_FNAME,index=True)