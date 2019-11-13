"""
Fisher zscore all r values from correlations-zscore.py
and derived pvalues as as the proportion of fisher
zscored R values that are above 0.

Export dataframe holding the final stats
and correlation parameters.

Also resaves out the resampling file, now with
just an additional column for the fisher zscores.
"""
from os import path
from json import load
import pandas as pd

from statsmodels.stats.multitest import multipletests


# load results directory from configuration file
with open('./config.json') as f:
    p = load(f)
    RES_DIR  = path.expanduser(p['results_directory'])
# choose params to make 95% confidence intervals
CI_LO = .025
CI_HI = .975


#######  load and manipulate data  #######

infname = path.join(RES_DIR,'correlations-data.tsv')
res_df = pd.read_csv(infname,sep='\t',index_col=['probe','resample'])


#######  derive pvalues  #######

# fisher zscore all r values
def fisherz(x):
    # arctanh can't handle -1 or 1 so this function accounts for that
    if x in [-1,1]:
        # multiply by x to 
        x -= pd.np.sign(x) * .000001 # picked 6 decimal points bc that's the precision of other values
    return pd.np.arctanh(x)
res_df['rfishz'] = res_df['r'].map(fisherz)

# initialize stats dataframe with the mean of each metric
stats_df = res_df.groupby('probe').mean()
stats_df.columns = [ f'{c}_mean' for c in stats_df.columns ]
# add confidence intervals for r ans fisherz r values
for col in ['r','rfishz']:
    stats_df[f'{col}_cilo'] = res_df.groupby('probe')[col].quantile(CI_LO)
    stats_df[f'{col}_cihi'] = res_df.groupby('probe')[col].quantile(CI_HI)

# add pvalue based on fisher zscore
stats_df['pval'] = res_df.groupby('probe').agg({'rfishz':lambda col: pd.np.mean(col<0)})

# generate a pvalue accounting for multiple comparisons
uncorrected_pvals = stats_df['pval'].values
mc_results = multipletests(uncorrected_pvals,
    alpha=0.05,method='fdr_bh',is_sorted=False,returnsorted=False)
sig, corrp, alphacSidak, alphacBonf = mc_results
stats_df['pval_corrected'] = corrp


########  export dataframes  ########

# round values while also changing output format to print full values
for df in [stats_df,res_df]:
    for col in df.columns:
        fmt = '%.04f' if 'pval' in col else '%.02f'
        df[col] = df[col].map(lambda x: fmt % x)

stats_fname = path.join(RES_DIR,'correlations-stats.tsv')
stats_df.to_csv(stats_fname,index=True,sep='\t')

res_df.to_csv(infname,index=True,sep='\t')
