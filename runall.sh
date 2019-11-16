# Directory structure is pull from the configuration file (`config.json`),
# so check that before running anything.


# convert original raw data file from excel to csv, and clean it up a bit
python cleandata.py

# get descriptive statistics/plots for the whole DLQ/MUSK questionnaire
python dlq_descriptives.py

# quantify lucid dream induction success
python induction_success-freq_table.py # generate a frequency table used by following scripts
python induction_success.py            # plot aggregated data
python induction_success-indiv.py      # plot subjects individually
python induction_success-cutoffs.py    # plot proportions of aggregated data at diff cutoffs/criterion

# run ordinal regression model predicting lucidity with induction method aspects
Rscript regression-model.R             # run model and output results
python regression-plot_dv.py           # plot model probability estimates for MILD
python regression-plot_iv.py           # plot scatterplots of relationship between predictors and lucidity

# run correlations between DLQ1 and some other things of interest
python correlations-resample.py
python correlations-zscore.py
python correlations-plot.py

# export text files that put digestible structure dream reports and open questions
python group_openquestions.py