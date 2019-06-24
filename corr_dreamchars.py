"""
Run correlations between DLQ1 and reported dream characteristics.
"""

from os import path
import tqdm
import pandas as pd


datadir = path.expanduser('~/IDrive-Sync/proj/phenol/data')
resdir  = path.expanduser('~/IDrive-Sync/proj/phenol/results')

infname = path.join(datadir,'data-clean.tsv')
outfname = path.join(resdir,'resampled_correlations.tsv')


df = pd.read_csv(infname,sep='\t')

df = df[df['dreamreport:1']!='No recall']


# # does DLQ1 correlate with any dream characteristics
# char_cols = ['Neg Emo','Neg Body','Neg Mood',' Pos Emo',
#             'Pos Body','Pos Mood','Sensory','Bizarreness']

# import pingouin as pg
# pg.pairwise_corr(df,columns=dlq_cols,method='kendall')

# pg.pairwise_corr(df,columns=[['DLQ:1'],char_cols],
#                  method='kendall',padjust='fdr_bh')

cols_of_interest = ['Sensory','Bizarreness']
res_df = pd.DataFrame(index=cols_of_interest,
                      columns=['r','loci','hici','pval'])

for col in tqdm.tqdm(cols_of_interest,desc='resampling correlations'):
    rvals = []
    for i in tqdm.trange(1000,desc=col):
        r = df.groupby('subj').apply(lambda df: df.sample(1)
            )[['DLQ:1',col]].corr(method='kendall').values[0,1]
        # x = tdf[col]
        # y = tdf['DLQ:1']
        # slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
        rvals.append(r)
    rmean = pd.np.mean(rvals)
    loci, hici = pd.np.percentile(rvals,[2.5,97.5])
    fishz_rs = pd.np.arctanh(rvals)
    pval = pd.np.mean(fishz_rs<0)
    res_df.loc[col,['r','loci','hici','pval']] = rmean, loci, hici, pval
    # res_df.loc[col,['intercept','slope']] = slope, intercept

res_df.to_csv(outfname,sep='\t',index=True,index_label='var')
