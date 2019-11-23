"""
Subtract 1 from all Likert responses.

Also convert from xls to tsv file.
That could be done from excel but just do it here,
and from excel the tsv requires encoding="ISO-8859-1"
when loading in with pandas.

Start with the cleaned excel file.
"""
from os import path
from json import load
import pandas as pd

with open('./config.json') as f:
    p = load(f)
    DATADIR = path.expanduser(p['data_directory'])


# load data
infname  = path.join(DATADIR,'data-clean.xls')
outfname = path.join(DATADIR,'data.tsv')
df = pd.read_excel(infname)


# subtract 1 from all Likert scale responses
likert_cols = []
for col in df.columns:
    if ('PANAS' in col
     or 'DLQ'   in col
     or 'MUSK'  in col
     or 'CHAR'  in col):
        likert_cols.append(col)

df[likert_cols] -= 1


# clearly indicate rows without dream recall
# by making them NaNs so easier to drop later
df.replace(dict(dream_report={'No recall':pd.np.nan}),inplace=True)


# add session column denoting the nth entry within subjects
df['session_id'] = pd.np.nan
subjcounts = df['participant_id'].value_counts().to_dict()
df.set_index('participant_id',inplace=True)
for sub, subcounts in subjcounts.items():
    df.loc[sub,'session_id'] = range(subcounts)
df.reset_index(drop=False,inplace=True)
df['session_id'] += 1


# create a night_id that has subject and night in it
df['session_id'] = df['session_id'].astype(int)
df['night_id'] = df.apply(
    lambda row: '{}-{}'.format(row['participant_id'],row['session_id']),axis=1)


df.to_csv(outfname,sep='\t',index=False,float_format='%.0f',na_rep=pd.np.nan)