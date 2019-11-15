"""
Age and sex descriptives (print them out)
"""
from os import path
from json import load
import pandas as pd

with open('./config.json') as f:
    p = load(f)
    data_dir = path.expanduser(p['data_directory'])

participant_fname = path.join(data_dir,'participants.tsv')

df = pd.read_csv(participant_fname,sep='\t')

print('\n***************** AGE *****************')
print(df['age'].describe().round(2).to_string())

print('\n***************** GENDER *****************')
print(pd.Categorical(df['gender']).describe().to_string())