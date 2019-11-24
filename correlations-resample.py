"""
Run all correlations (of interest) with DLQ1.

Things to correlate with DLQ1:
    - all things on morning survey about the dream
      (e.g., bizarreness)
    - positive and negative PANAS summary scores
      (from each morning)
    - dream control score (derived from DLQ/MUSK)

There are multiple subject datapoints so can't just run a
simple correlation because datapoints are not independent.

So for each correlation, run a resampling procedure
where for every iteration, one sample is drawn randomly
per subject and a normal correlation is run across
points (bc now there is only one datapoint per subject).
For each dream characteristic, run N iterations.

Fisher zscoring and pvalues come from correlations-zscore.py

Export dataframe holding all the resampled correlations

"""
from os import path
from json import load
import tqdm
import pandas as pd

pd.np.random.seed(72) # for reproducibility

# load analysis parameters from configuration file
with open('./config.json') as f:
    p = load(f)
    DATA_DIR = path.expanduser(p['data_directory'])
    RES_DIR  = path.expanduser(p['results_directory'])
    POS_PROBES = p['PANAS_positive_probes']
    NEG_PROBES = p['PANAS_negative_probes']
    CONTROL_PROBES = p['DLQ_control_probes']
    N_RESAMPLES = p['n_correlation_resamples']
    FMT = p['float_formatting']


#######  load and manipulate data  #######

infname = path.join(DATA_DIR,'data.tsv')
df = pd.read_csv(infname,sep='\t')

# drop all nights without recall
df.dropna(subset=['dream_report'],axis=0,inplace=True)

# pick columns to run correlation on
cols2corr = [ col for col in df.columns if 'CHAR' in col ]
cols2corr.append('PANAS_pos')
cols2corr.append('PANAS_neg')
cols2corr.append('sleep_quality')
cols2corr.append('dream_control')

# generate columns that require manipulations of the raw data
panas_pos_cols = [ f'PANAS_{x:02d}' for x in POS_PROBES ]
panas_neg_cols = [ f'PANAS_{x:02d}' for x in NEG_PROBES ]
control_cols   = [ f'DLQ_{x:02d}' for x in CONTROL_PROBES ]
df['PANAS_pos']     = df[panas_pos_cols].sum(axis=1)
df['PANAS_neg']     = df[panas_neg_cols].sum(axis=1)
df['dream_control'] = df[control_cols].mean(axis=1)


#######  analysis  #######

# build dataframe to hold all the resampled correlations
METRICS = ['slope','intercept','tau']
INDEX_NAMES = ['probe','resample']
index_values = [cols2corr,range(N_RESAMPLES)]
index = pd.MultiIndex.from_product(index_values,names=INDEX_NAMES)
res_df = pd.DataFrame(columns=METRICS,index=index,dtype=float)

# loop over each variable of interest and run N
# correlations, resampling a random night from
# each participant every time
for col in tqdm.tqdm(cols2corr,desc='resampling correlations'):
    # if it's one of the CHAR columns, then the
    # 0 option is "no recall" so take that out
    if 'CHAR' in col:
        subdf = df[ df[col] > 0]
    for i in tqdm.trange(N_RESAMPLES,desc=col):
        # sample one night from each subject, randomly
        rsmpl_df = subdf.groupby('participant_id').apply(
            lambda df: df.sample(1))[['DLQ_01',col]]
        # correlate col/var with DLQ1
        r = rsmpl_df.corr(method='kendall').values[0,1]
        # get the slope/intercept for later plotting
        x = rsmpl_df[col].values
        y = rsmpl_df['DLQ_01'].values
        m, b = pd.np.polyfit(x,y,1)
        # save to dataframe
        res_df.loc[(col,i),METRICS] = [m,b,r]


########  export  ########

# round values while also changing output format to print full values
for col in res_df.columns:
    res_df[col] = res_df[col].map(lambda x: FMT % x)
res_fname = path.join(RES_DIR,'correlations-data.tsv')
res_df.to_csv(res_fname,index=True,sep='\t')

print('\n') # clear last terminal line