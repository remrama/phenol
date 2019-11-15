"""
The original response options were very open-ended,
which resulted in some unique responses that need
to be changed to fit with the rest.

Importantly, this also DROPS some rows that are unclear.
1. where dreamreport was left blank (ie, not just no recall)
2. where bedtime was unclear

Also importantly, this REPLACES NaNs in a few columns
that I think can safely be interpreted as zeros.
1. Min MILD
2. Min Awake

Export as .tsv file because of commas in the text entries.
"""
from os import path
from json import load
import pandas as pd


with open('./config.json') as f:
    p = load(f)
    DATA_DIR = path.expanduser(p['data_directory'])

infname = path.join(DATA_DIR,'data-raw.xls')
outfname = infname.replace('-raw.xls','-clean.tsv')

df = pd.read_excel(infname)

# Make a dictionary that has column names as keys,
# and another dictionary as items, where the
# secondary dict has (oldval,newval) as (key,val) pairs.
replace_dict = {

    'BedTime': {
        4.3 : pd.datetime.time(pd.to_datetime('4:30',format='%H:%M')),
        100 : pd.datetime.time(pd.to_datetime('1:00',format='%H:%M')),
        2300 : pd.datetime.time(pd.to_datetime('23:00',format='%H:%M')),
        2000 : pd.datetime.time(pd.to_datetime('20:00',format='%H:%M')),
        10 : pd.np.nan, # NOT SURE WHAT TO DO WITH THIS ONE. TEN????
        2345 : pd.datetime.time(pd.to_datetime('23:45',format='%H:%M')),
        '02;00' : pd.datetime.time(pd.to_datetime('2:00',format='%H:%M')),
        '03:00am' : pd.datetime.time(pd.to_datetime('3:00',format='%H:%M')),
        '3:30am' : pd.datetime.time(pd.to_datetime('3:30',format='%H:%M')),
        '4:45am' : pd.datetime.time(pd.to_datetime('4:45',format='%H:%M')),
    },

    'Rise Time': {
        '16:00 pm' : pd.datetime.time(pd.to_datetime('16:00',format='%H:%M')),
        '10:15am' : pd.datetime.time(pd.to_datetime('10:15',format='%H:%M')),
        '10:30am' : pd.datetime.time(pd.to_datetime('10:30',format='%H:%M')),
        930 : pd.datetime.time(pd.to_datetime('9:30',format='%H:%M')),
        645 : pd.datetime.time(pd.to_datetime('6:45',format='%H:%M')),
        400 : pd.datetime.time(pd.to_datetime('4:00',format='%H:%M')),
        900 : pd.datetime.time(pd.to_datetime('9:00',format='%H:%M')),
        1030 : pd.datetime.time(pd.to_datetime('10:30',format='%H:%M')),
    },

    'Out of Bed': {
        '18:45pm' : pd.datetime.time(pd.to_datetime('18:45',format='%H:%M')),
        '11:00am' : pd.datetime.time(pd.to_datetime('11:00',format='%H:%M')),
        '10:30am' : pd.datetime.time(pd.to_datetime('10:30',format='%H:%M')),
        '11:00am' : pd.datetime.time(pd.to_datetime('11:00',format='%H:%M')),
        '11:15am' : pd.datetime.time(pd.to_datetime('11:15',format='%H:%M')),
        '10:40am' : pd.datetime.time(pd.to_datetime('10:40',format='%H:%M')),
        1035 : pd.datetime.time(pd.to_datetime('10:35',format='%H:%M')),
        1000 : pd.datetime.time(pd.to_datetime('10:00',format='%H:%M')),
        650 : pd.datetime.time(pd.to_datetime('6:50',format='%H:%M')),
        600 : pd.datetime.time(pd.to_datetime('6:00',format='%H:%M')),
        915 : pd.datetime.time(pd.to_datetime('9:15',format='%H:%M')),
    },

    'MILD Time': {
        '4:30am' : pd.datetime.time(pd.to_datetime('4:30',format='%H:%M')),
        '7am' : pd.datetime.time(pd.to_datetime('7:00',format='%H:%M')),
        '5:15qn' : pd.datetime.time(pd.to_datetime('5:15',format='%H:%M')),
        '7:00am' : pd.datetime.time(pd.to_datetime('7:00',format='%H:%M')),
        '6:00am' : pd.datetime.time(pd.to_datetime('6:00',format='%H:%M')),
        '9am' : pd.datetime.time(pd.to_datetime('9:00',format='%H:%M')),
        130 : pd.datetime.time(pd.to_datetime('1:30',format='%H:%M')),
        120 : pd.datetime.time(pd.to_datetime('1:20',format='%H:%M')),
        2310 : pd.datetime.time(pd.to_datetime('23:10',format='%H:%M')),
        2010 : pd.datetime.time(pd.to_datetime('20:10',format='%H:%M')),
        15 : pd.np.nan, # NOT SURE WHAT TO DO WITH THIS ONE. FIFTEEN????
        2345 : pd.datetime.time(pd.to_datetime('23:45',format='%H:%M')),
        '-' : pd.np.nan,
        'n/a' : pd.np.nan,
        'N?A' : pd.np.nan,
    },

    ## NOTE: here inserting NaNs and then replacing later.
    ## Do it this way because sometimes these are read in as NaNs.
    'Min MILD': {
        pd.datetime.time(pd.to_datetime('12',format='%H')) : 12,
        '1 or 2 mins' : 1.5,
        'around 2' : 2,
        'a minute' : 1,
        'Roughly 10' : 10,
        '-' : pd.np.nan,
        'N/A' : pd.np.nan,
        'n/a' : pd.np.nan,
    },

    ## NOTE: here inserting NaNs and then replacing later.
    ## Do it this way because sometimes these are read in as NaNs.
    'Min Awake': {
        'around 10' : 10,
        'not sure but less than 10 mins' : 9,
        'half hour' : 30,
        'unsure' : pd.np.nan,
        '90-120' : 105,
        'Around 15' : 15,
        '-' : pd.np.nan,
    },

    'dreamreport:1': {
        'No Recall': 'No recall',
        'no recall': 'No recall',
        'No Recall ': 'No recall',
        'no recall ': 'No recall',
        'No recall ': 'No recall',
    }

}

# replace the values
df.replace(replace_dict,inplace=True)


# replace some NaNs with zero
fillna_cols = ['Min MILD','Min Awake']
replace_val = 0
for col in fillna_cols:
    df[col].fillna(replace_val,inplace=True)

# some that had strings need to be converted
df['Min MILD'] = df['Min MILD'].astype(float)
df['Min Awake'] = df['Min Awake'].astype(float)


### Other technique?
# Most subjs have some form of "No" entered here,
# but someone put a 1?? and another kept putting
# a form of "Reality checks", which everyone is
# already doing. So these are all NO.
df['other'] = 0


# drop NaNs
nacheck_cols = ['dreamreport:1','BedTime']
df.dropna(subset=nacheck_cols,axis='rows',how='any',inplace=True)



# check stuff
intcolumns = ['Code','#Reality Check','Min MILD','Min Awake']
for col in intcolumns:
    # assert not df[col].isnull().any()
    assert df[col].dtype in [pd.np.int64,pd.np.float64]

from datetime import time
checktime = lambda x: isinstance(x,time)
timecolumns = ['BedTime','MILD Time']
for col in timecolumns:
    assert df[col].dropna().apply(checktime).all()


def checkrecall(row):
    if pd.np.isnan(row['DLQ:1']):
        assert row['dreamreport:1'] == 'No recall'

_ = df.apply(checkrecall,axis=1)



# rather have subj as int than float
df['Code'] = df['Code'].astype(int)



#####  Column renaming  #####
rename_dict = {
    'Code' : 'subj',
    '#Reality Check' : 'n_rcs',
    'BedTime' : 'bedtime',
    'MILD Time' : 'mildtime',
    'Min MILD' : 'mildlength',
    'Min Awake' : 'wbtblength',
    'Other technique?' : 'other',
    'Rise Time' : 'waketime',
    'Out of Bed' : 'outofbedtime',
    'Sleep Quality' : 'sleepquality',
}
df.rename(columns=rename_dict,inplace=True)


# add "session" column denoting the nth entry within subjects
df['sess'] = pd.np.nan
subjcounts = df['subj'].value_counts().to_dict()
df.set_index('subj',inplace=True)
for sub, subcounts in subjcounts.items():
    df.loc[sub,'sess'] = range(subcounts)
df.reset_index(drop=False,inplace=True)


# add recoded time columns that center on 24:00 (for regression)
for timecol in ['bedtime','waketime','outofbedtime']:
    df[f'{timecol}_int'] = df[timecol
        ].apply(lambda x: x.hour + x.minute/60.
        ).apply(lambda x: x-24 if x>12 else x) 


df.to_csv(outfname,sep='\t',index=False,na_rep=pd.np.nan)
