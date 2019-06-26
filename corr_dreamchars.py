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

# pick the columns of interest
DREAM_CHR_COLS = ['Sensory','Neg Emo','Neg Body','Neg Mood',
                  'Bizarreness',' Pos Emo','Pos Body','Pos Mood']
METRICS = ['slope','intercept','fishz_r']
res_df = pd.DataFrame(index=DREAM_CHR_COLS,columns=METRICS)

for col in tqdm.tqdm(DREAM_CHR_COLS,desc='resampling correlations'):
    resampled_vals = { metric: [] for metric in METRICS }
    for i in tqdm.trange(1000,desc=col):
        # r = df.groupby('subj').apply(lambda df: df.sample(1)
        #     )[['DLQ:1',col]].corr(method='kendall').values[0,1]
        rsmpl_df = df.groupby('subj').apply(lambda df: df.sample(1))[['DLQ:1',col]]
        x = rsmpl_df[col].values
        y = rsmpl_df['DLQ:1'].values
        rval = pd.np.arctanh(rsmpl_df.corr(method='kendall').values[0,1])
        m, b = pd.np.polyfit(x,y,1)
        results = [m,b,rval]
        for metric, value in zip(METRICS,results):
            resampled_vals[metric].append(value)
    for metric in METRICS:
        res_df.loc[col,metric] = pd.np.mean(resampled_vals[metric])
    res_df.loc[col,'pval'] = pd.np.mean(pd.np.asarray(resampled_vals['fishz_r'])<0)
    # rmean = pd.np.mean(rvals)
    # loci, hici = pd.np.percentile(rvals,[2.5,97.5])
    # fishz_rs = pd.np.arctanh(rvals)
    # pval = pd.np.mean(fishz_rs<0)
    # res_df.loc[col,['r','loci','hici','pval']] = rmean, loci, hici, pval
    # res_df.loc[col,['intercept','slope']] = intercept, slope

res_df.to_csv(outfname,sep='\t',index=True,index_label='var')
