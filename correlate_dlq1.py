"""
Run all correlations (of interest) with DLQ1.

Things to correlate with DLQ1:
    - all things on morning survey about the dream
      (e.g., bizarreness)
    - positive and negative PANAS summary scores
      (from each morning)
    - dream control score (derived from DLQ/MUSK)

There are multiple subject datapoints so can't just
run a simple correlation because datapoints are not
independent.

So for each correlation, run a resampling procedure
where for every iteration, one sample is drawn
randomly per subject and a normal correlation is run
across those points (bc now there is only one
datapoint per subject). For each dream characteristic,
run N iterations and get a pvalue as the proportion
of fisher zscored R values that are above 0.

Export 2 dataframes:
    1. holds all the resampled correlations
    2. holds the final stats and correlation parameters
"""
from os import path
from json import load
import tqdm
import pandas as pd

from statsmodels.stats.multitest import multipletests


# load analysis parameters from configuration file
with open('./config.json') as f:
    p = load(f)
    datadir = path.expanduser(p['data_directory'])
    resdir  = path.expanduser(p['results_directory'])
    pos_probes = p['PANAS_positive_probes']
    neg_probes = p['PANAS_negative_probes']
    control_probes = p['DLQ_control_probes']
    n_resamples = p['n_correlation_resamples']
    cols2corr = p['variables_to_correlate']


#######  load and manipulate data  #######

infname = path.join(datadir,'data-clean.tsv')
df = pd.read_csv(infname,sep='\t')

# drop all nights without recall
df = df[df['dreamreport:1']!='No recall']

# generate columns that require manipulations
# of the raw data
panas_pos_cols = [ f'Affect:{x}' for x in pos_probes ]
panas_neg_cols = [ f'Affect:{x}' for x in neg_probes ]
control_cols   = [ f'DLQ:{x}' for x in control_probes ]
df['panas_pos']     = df[panas_pos_cols].mean(axis=1)
df['panas_neg']     = df[panas_neg_cols].mean(axis=1)
df['dream_control'] = df[control_cols].mean(axis=1)


#######  analysis  #######

# build dataframe to hold all the resampled correlations
METRICS = ['slope','intercept','r']
index_values = [cols2corr,range(n_resamples)]
index_names = ['probe','resample']
index = pd.MultiIndex.from_product(index_values,names=index_names)
res_df = pd.DataFrame(columns=METRICS,index=index,dtype=float)

# loop over each variable of interest and run N
# correlations, resampling a random night from
# each participant every time
for col in tqdm.tqdm(cols2corr,desc='resampling correlations'):
    for i in tqdm.trange(n_resamples,desc=col):
        # sample one night from each subject, randomly
        rsmpl_df = df.groupby('subj').apply(lambda df: df.sample(1))[['DLQ:1',col]]
        # correlate col/var with DLQ1
        r = rsmpl_df.corr(method='kendall').values[0,1]
        # get the slope/intercept for later plotting
        x = rsmpl_df[col].values
        y = rsmpl_df['DLQ:1'].values
        m, b = pd.np.polyfit(x,y,1)
        # save to dataframe
        res_df.loc[(col,i),METRICS] = [m,b,r]

# fisher zscore all r values
def fisherz(x):
    # arctanh can't handle -1 or 1 so this function accounts for that
    if x in [-1,1]:
        # multiply by x to 
        x -= pd.np.sign(x) * .000001 # picked 6 decimal points bc that's the precision of other values
    return pd.np.arctanh(x)
res_df['rfishz'] = res_df['r'].map(fisherz)

# choose params to make 95% confidence intervals
CI_LO = .025
CI_HI = .975
# initialize stats dataframe with the mean of each metric
stats_df = res_df.groupby('probe').mean()
stats_df.columns = [ f'{c}_mean' for c in stats_df.columns ]
# add confidence intervals for r ans fisherz r values
for col in ['r','rfishz']:
    stats_df[f'{col}_cilo'] = res_df.groupby('probe')[col].quantile(CI_LO)
    stats_df[f'{col}_cihi'] = res_df.groupby('probe')[col].quantile(CI_HI)
# res_df.groupby('probe').agg(pd.np.quantile,q=CI_LO)
# res_df.groupby('probe').agg(pd.np.quantile,q=CI_HI)

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
for df in [res_df,stats_df]:
    for col in df.columns:
        fmt = '%.04f' if col == 'pval' else '%.02f'
        df[col] = df[col].map(lambda x: fmt % x)

res_fname = path.join(resdir,'correlate_dlq1-data.tsv')
res_df.to_csv(res_fname,index=True,sep='\t')
stats_fname = path.join(resdir,'correlate_dlq1-stats.tsv')
stats_df.to_csv(stats_fname,index=True,sep='\t')

print('\n') # clear last terminal line