"""
The data file has each dream report and the corresponding
open-ended questions within each row.

For the qualitative peak into the open-ended questions and
how they relate to dreams and lucidity (DLQ1) ratings, it's
better to have them in a more digestible structure.

So here, take each night's dream report, open question
responses, and DLQ1 response, and export 2 text files:
    1. one that lists responses to each open question, grouped by DLQ1
        So OpenQs > DLQ1 > response
        <openqs-byprobe.txt>
    2. one that groups all open questions by lucidity rating
        Sp DLQ1 > OpenQs > response
        <openqs-byresponse.txt>
"""
from os import path
from json import load
import pandas as pd

from collections import OrderedDict


with open('./config.json') as f:
    p = load(f)
    datadir = path.expanduser(p['data_directory'])
    resdir  = path.expanduser(p['results_directory'])


COLS2KEEP = ['night_id','DLQ_01','dream_report',
    'INTERR_1','INTERR_2','INTERR_3','INTERR_4']
fname = path.join(datadir,'data.tsv')
df = pd.read_csv(fname,usecols=COLS2KEEP,sep='\t')


# drop nights without dream recall
df.dropna(subset=['dream_report'],axis=0,inplace=True)

df['DLQ_01'] = df['DLQ_01'].astype(int)

df.rename(columns={'dream_report':'INTERR_0'},inplace=True)


ID_COLS = ['night_id','DLQ_01']
VAL_COLS = [ f'INTERR_{x}' for x in range(5) ]
melted_df = df.melt(id_vars=ID_COLS,value_vars=VAL_COLS,
                    var_name='probe',value_name='response')

# OPEN_QUESTIONS = OrderedDict([
#     ('dreamreport:1' , "Dream report"),
#     ('Open:1'        , "What level of awareness did you select for the statement I was aware that I was dreaming on a scale of 0-4? Why did you rate your awareness at the value you did?"),
#     ('Open:2'        , "What kind of experience(s) gave you an impression of your selected level of awareness?"),
#     ('Open:3'        , "If you did not select 4 (full awareness), why not? What prevented you from attributing full awareness to your dream?"),
#     ('Open:4'        , "Describe the sections of your dream report that were relevant to your responding to this question, and explain why."),
# ])

SORT_ORDERS = dict(byresp=['DLQ_01','probe'],
                   byprobe=['probe','DLQ_01'])

for key, sort_order in SORT_ORDERS.items():
    top_col, bot_col = sort_order
    text = ''
    
    for top_id, top_df in melted_df.groupby(top_col):
        text += f'{top_id}\n'

        for bot_id, bot_df in top_df.groupby(bot_col):
            text += f'\t{bot_id}\n'

            for night_id, night_df in bot_df.groupby('night_id'):
                assert len(night_df) == 1
                response = night_df['response'].values[0]
                text += f'\t\t{night_id} : {response}\n'

    export_fname = path.join(resdir,f'openqs-{key}.txt')
    with open(export_fname,'w') as outfile:
        outfile.write(text)