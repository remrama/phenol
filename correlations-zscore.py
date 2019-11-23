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
import numpy as np
import pandas as pd

from statsmodels.stats.multitest import fdrcorrection


# load results directory from configuration file
with open('./config.json') as f:
    p = load(f)
    RES_DIR  = path.expanduser(p['results_directory'])
    FMT = p['float_formatting']
    N_RESAMPLES = p['n_correlation_resamples']
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
        x -= np.sign(x) * .000001 # picked 6 decimal points bc that's the precision of other values
    return np.arctanh(x)
res_df['fishz'] = res_df['tau'].map(fisherz)

# initialize stats dataframe with the mean of each metric
stats_df = res_df.groupby('probe').mean()
stats_df.columns = [ f'{c}_mean' for c in stats_df.columns ]
# get confidence intervals for fisherz values
stats_df['fishz_cilo'] = res_df.groupby('probe')['fishz'].quantile(CI_LO)
stats_df['fishz_cihi'] = res_df.groupby('probe')['fishz'].quantile(CI_HI)

# add pvalue based on fisher zscore
def calculate_pvalue(col):
    # p = % of values > or < 0
    # double the smaller p value (bc two-tailed test)
    proportion_above = np.mean( col.values > 0 )
    proportion_below = np.mean( col.values < 0 )
    above_or_below = min([proportion_above,proportion_below])
    pval = 2 * above_or_below
    return pval
stats_df['pval'] = res_df.groupby('probe').agg({'fishz':calculate_pvalue})

# generate a pvalue accounting for multiple comparisons
uncorrected_pvals = stats_df['pval'].values
_, corrp = fdrcorrection(uncorrected_pvals,method='indep',is_sorted=False)
stats_df['pval_corrected'] = corrp


########  export dataframes  ########

# round values while also changing output format to print full values
for df in [stats_df,res_df]:
    for col in df.columns:
        df[col] = df[col].map(lambda x: FMT % x)

stats_fname = path.join(RES_DIR,'correlations-stats.tsv')
stats_df.to_csv(stats_fname,index=True,sep='\t')

res_df.to_csv(infname,index=True,sep='\t')
