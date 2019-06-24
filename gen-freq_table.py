"""
Get subject frequency counts for each
response value/option of DLQ for question 1.

Exports tsv table.
"""
from os import path
import pandas as pd

datadir = path.expanduser('~/DBp/proj/phenol/data')
resdir = path.expanduser('~/DBp/proj/phenol/results')

infname = path.join(datadir,'data-clean.tsv')
outfname = path.join(resdir,'dlq1-frequency.tsv')

indf = pd.read_csv(infname,sep='\t')

outdf = indf.groupby('subj')['DLQ:1'
    ].value_counts(dropna=False
    ).unstack(fill_value=0)

outdf.columns = [ 'No recall' if pd.np.isnan(x) 
                              else 'DLQ1_resp-{:.0f}'.format(x)
                   for x in outdf.columns ]

assert len(outdf.columns) == 6, 'Not all resp options present'

outdf.to_csv(outfname,index=True,sep='\t')



# # get value counts of each DLQ response for each subj
# respoptions = [pd.np.nan,1,2,3,4,5]
# indx = pd.MultiIndex.from_product([df['subj'].unique(),respoptions],
#                                    names=['subj','DLQ:1'])
# grouped = df.groupby('subj')['DLQ:1'
#         ].value_counts(dropna=False,sort=True
#         ).reindex(indx,fill_value=0 # zeros when a subj never chose a resp
#         ).rename('count'      # so resetting works
#         ).reset_index(drop=False    # so NaNs can be replaced
#         ).rename(columns={'DLQ:1':'response'}
#         )
# # pivot to wide format for row-per-subj
# pivoted = grouped.pivot(index='subj',
#                         columns='response',
#                         values='count')

