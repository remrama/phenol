"""
For readability, convert dream reports
from clean tsv file to single txt file.
"""

from os import path
import pandas as pd
from collections import OrderedDict


datadir = path.expanduser('~/DBp/proj/phenol/data')
resdir  = path.expanduser('~/DBp/proj/phenol/results')
infname = path.join(datadir,'data-clean.tsv')
outfname = path.join(resdir,'dream-reports.txt')

df = pd.read_csv(infname,index_col='subj',sep='\t')

open_cols = [ f'Open:{i}' for i in [1,2,3,4] ]

txtout = ''
for resp, respdf in df.groupby('DLQ:1'):
    txtout += f'DLQ response {resp:.0f}\n'
    for subj, row in respdf.iterrows():
        drmreport = row['dreamreport:1']
        txtout += f'\tDream report : {drmreport} (sub-{subj:03d})\n'
        for col in open_cols:
            answ = row[col]
            txtout += f'\t\t{col} : {answ}\n'
    txtout += '\n\n'

with open(outfname,'w') as outfile:
    outfile.write(txtout)