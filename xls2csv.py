"""
Convert original (albeit manually cleaned and deidentified) data format from excel to csv.

Also do some other tidying things:
    - Subtract 1 from all Likert responses, so they start at 0.
    - Replace non-dream entries with explicit NA representation.
    - Add a new column <session_id> that denotes the entry number for that participant.
    - Add a new column <night_id> that just combines participant_id and the session_id.
"""
from os import path
from json import load

import pandas as pd


with open('./config.json') as f:
    p = load(f)
    DATA_DIR = path.expanduser(p['data_directory'])

IMPORT_FNAME = path.join(DATA_DIR,'data-clean.xls')
EXPORT_FNAME = path.join(DATA_DIR,'data.csv')


# load data
df = pd.read_excel(IMPORT_FNAME,index_col='participant_id')

# subtract 1 from all Likert scale responses
likert_cols = [ col for col in df.columns
    if ('PANAS' in col
     or 'DLQ'   in col
     or 'MUSK'  in col
     or 'CHAR'  in col) ]
df[likert_cols] -= 1

# clearly indicate rows without dream recall by making them NaNs so easier to drop later
df.replace(dict(dream_report={'No recall':pd.NA}),inplace=True)

# add session_id column denoting the nth entry within each subject
df['session_id'] = pd.NA
for pp, n_sessions in df.index.value_counts().items():
    df.loc[pp,'session_id'] = range(1,n_sessions+1)

# create a night_id that has subject and night in it
df['night_id'] = df.index.astype(str) + '-' + df['session_id'].astype(str)

# save
df.to_csv(EXPORT_FNAME,index=True,float_format='%.0f',na_rep=pd.np.nan)