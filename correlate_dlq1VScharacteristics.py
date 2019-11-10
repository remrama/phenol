"""
Run correlations between DLQ1 and reported dream characteristics.

For each dream characteristic (bizarreness, positive emotion, etc.),
run a correlation with the same dream's DLQ1 response.

There are multiple subject datapoints so can't just run a simple
correlation because datapoints are not independent.

So for each correlation, run a resampling procedure where for
every iteration, one sample is drawn randomly per subject and
a normal correlation is run across those points (bc now there
is only one datapoint per subject). For each dream characteristic,
run 1000 iterations and get 2 pvalues (one per direction). Pvalues
are the proportion of fisher zscored R values that are above/below 0.

Export 2 dataframes, one that holds all the resampled correlations
and another that holds the final stats and correlation parameters.
"""
from os import path
import tqdm
import pandas as pd


N_RESAMPLES = 1000 # per dream characteristic

datadir = path.expanduser('~/DBp/proj/phenoll/data')
resdir  = path.expanduser('~/DBp/proj/phenoll/results')

infname = path.join(datadir,'data-clean.tsv')

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
METRICS = ['slope','intercept','r']
index = pd.MultiIndex.from_product([DREAM_CHR_COLS,range(N_RESAMPLES)],
                                    names=['probe','resample'])
res_df = pd.DataFrame(columns=METRICS,index=index,dtype=float)

for col in tqdm.tqdm(DREAM_CHR_COLS,desc='resampling correlations'):
    for i in tqdm.trange(N_RESAMPLES,desc=col):
        # r = df.groupby('subj').apply(lambda df: df.sample(1)
        #     )[['DLQ:1',col]].corr(method='kendall').values[0,1]
        # get the correlation value
        rsmpl_df = df.groupby('subj').apply(lambda df: df.sample(1))[['DLQ:1',col]]
        r = rsmpl_df.corr(method='kendall').values[0,1]
        # get the slope/intercept for plotting
        x = rsmpl_df[col].values
        y = rsmpl_df['DLQ:1'].values
        m, b = pd.np.polyfit(x,y,1)
        res_df.loc[(col,i),METRICS] = [m,b,r]
    # rmean = pd.np.mean(rvals)
    # loci, hici = pd.np.percentile(rvals,[2.5,97.5])
    # fishz_rs = pd.np.arctanh(rvals)
    # pval = pd.np.mean(fishz_rs<0)
    # res_df.loc[col,['r','loci','hici','pval']] = rmean, loci, hici, pval
    # res_df.loc[col,['intercept','slope']] = intercept, slope

# fisher zscore all r values
res_df['rfishz'] = res_df['r'].map(pd.np.arctanh)

CI_LO = .025
CI_HI = .975
# initialize stats dataframe with the mean of each metric
stats_df = res_df.groupby('probe').mean()
stats_df.columns = [ f'{c}_mean' for c in stats_df.columns ]
# add confidence intervals for fisher zscores
stats_df['rfishz_cilo'] = res_df.groupby('probe')['rfishz'].quantile(CI_LO)
stats_df['rfishz_cihi'] = res_df.groupby('probe')['rfishz'].quantile(CI_HI)
# res_df.groupby('probe').agg(pd.np.quantile,q=CI_LO)
# res_df.groupby('probe').agg(pd.np.quantile,q=CI_HI)

# add pvalue for fisher zscore
stats_df['pval'] = res_df.groupby('probe').agg({'rfishz':lambda col: pd.np.mean(col<0)})


# round values while also changing output format to print full values
for df in [res_df,stats_df]:
    for col in df.columns:
        fmt = '%.04f' if col == 'pval' else '%.02f'
        df[col] = df[col].map(lambda x: fmt % x)

res_fname = path.join(resdir,'correlate_characteristics-data.tsv')
res_df.to_csv(res_fname,index=True,sep='\t')
stats_fname = path.join(resdir,'correlate_characteristics-stats.tsv')
stats_df.to_csv(stats_fname,index=True,sep='\t')

print('\n') # clear last terminal line