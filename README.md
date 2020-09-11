## phenoll

Code for a research experiment investigating the phenomenology of semi-lucid dreams.

See `runall.sh` for a list of scripts and their purposes.

Three main analyses:
1. Lucid dreaming frequencies (within subjs) and rates (across subjs)
2. Regression with lucidity as outcome variable
3. Correlations between lucidity and other stuff

#### General sequence of scripts

```bash
# output folder is specified in the config.json file as "derivatives_dir"

# convert originel excel data to csv, with minor cleanup as well
# NOTE: this was used internally but any available data should already be in csv
python xls2csv.py             ## outputs <data_dir>/data.csv

# generate DLQ/MUSK descriptives dataframe and plot
python dlq_descriptives.py    ## outputs <derivatives_dir>/dlq.eps
                              ## outputs <derivatives_dir>/dlq.csv

# run frequencies analysis for LD induction success effects
python frequencies-generate_freqs.py  ## outputs <derivatives_dir>/ld_freqs.csv
python frequencies-indiv_subjs.py     ## outputs <derivatives_dir>/ld_freqs-subjs.csv
                                      ## outputs <derivatives_dir>/ld_freqs-subjs.svg
python frequencies-agg.py             ## outputs <derivatives_dir>/ld_freqs-plot.svg
python frequencies-cutoffs.py         ## outputs <derivatives_dir>/ld_freqs-cutoffs_data.csv
                                      ## outputs <derivatives_dir>/ld_freqs-cutoffs_stats.csv
                                      ## outputs <derivatives_dir>/ld_freqs-cutoffs_plot.svg

# run regression analysis for LD induction method adherence effects
Rscript regression-model.R            ## outputs <derivatives_dir>/adherence-coefficients.csv
                                      ## outputs <derivatives_dir>/adherence-stats.csv
python regression-plot_dv.py          ## outputs <derivatives_dir>/adherence-stats.svg
python regression-plot_iv.py          ## outputs <derivatives_dir>/adherence.svg

# run correlation analysis to see what is related to lucidity
python correlations-resample.py       ## outputs <derivatives_dir>/correlates.csv
python correlations-zscore.py         ## outputs <derivatives_dir>/correlates_withz.csv
                                      ## outputs <derivatives_dir>/correlates-stats.csv
python correlations-plot.py           ## outputs <derivatives_dir>/correlates-plot.svg
                                      ## outputs <derivatives_dir>/correlates-plot_zs.svg

# export text files that put digestible structure dream reports and open questions
python group_openquestions.py         ## outputs <derivatives_dir>/open_questions-by_probe.txt
                                      ## outputs <derivatives_dir>/open_questions-by_response.txt

# print out participant demographics if you want
python participant_descriptives.py    ## just prints
```