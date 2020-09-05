### Ordinal regression model predicting a single
### DLQ response (question 1: I was aware that I
### was dreaming).
###
### Outputs a table of the regression coefficients
### and also model prediction values based on the 
### significant effect of MILD.

suppressPackageStartupMessages(library(ordinal))
suppressPackageStartupMessages(library(effects))
suppressPackageStartupMessages(library(MASS))
suppressPackageStartupMessages(library(rjson))


# load data
datadir <- fromJSON(file='./config.json')$data_directory
derivdir <- fromJSON(file='./config.json')$derivatives_directory
fname <- paste(datadir,"data.csv",sep="/")
data <- read.csv(fname,na.strings="NA")
# # only use those rows with dream recall
# data = data[!is.na(data$dream_report),]
data = data[!is.na(data$DLQ_01),] # a few rows with recall but no DLQ

# make sure factors are factors
data$participant_id <- factor(data$participant_id)
data$DLQ_01 <- factor(data$DLQ_01,ordered=TRUE)


# summary(pac_1 <- polr(perceived_acad_success ~ fusion_t1_z, study1_t1, Hess = T)) 
# ctable_pac_1 <- coef(summary(pac_1)) #store the coefficient table
# p_pac_1 <- pnorm(abs(ctable_pac_1[, "t value"]), lower.tail = FALSE) * 2 #calculate p-values
# ctable_pac_1 <- cbind(ctable_pac_1, "p value" = p_pac_1) #combine back with the table
# exp(coef(pac_1)) #get Odds Ratio (OR)
# ci_pac_1 <- confint(pac_1) #get OR CI
# exp(cbind(OR = coef(pac_1), ci_pac_1))
# # we used this format to report the results:
# # OR = 1.42, 95% CI [1.25, 1.61], p < .0001
# exp(coef(model.fit))
# exp(confint(model.fit))

# build/run ordinal regression
model.fit <- clmm(DLQ_01 ~ (1|participant_id)
    + n_reality_checks + MILD_rehearsal_min + MILD_awake_min,
    data=data)
print(summary(model.fit))
# get odds ratios by taking exponent of the coefficients
# (makes coeffs interpretable)
outdf <- exp(cbind(OddsRatio=coef(model.fit),confint(model.fit)))
# add pvalue from regression model
outdf <- cbind(outdf,pval=summary(model.fit)$coefficients[,"Pr(>|z|)"])
# drop the useless stuff and export
predictors = c("n_reality_checks","MILD_rehearsal_min","MILD_awake_min")
outdf <- outdf[predictors,]
# export ordinal regression model
outdf = round(outdf,digits=3)
outfname <- paste(derivdir,"adherence-coefficients.csv",sep="/")
write.table(outdf,file=outfname,row.names=TRUE,col.names=NA,sep=",")


#### export model predictions for plotting in python

mildlength_vals <- 0:20
effdata <- Effect(focal.predictors=c("MILD_rehearsal_min"),mod=model.fit,
                  xlevels=list(MILD_rehearsal_min=mildlength_vals))

outeffdata <- effdata["prob"]$prob
# add col denoting mildlength used for model prediction
outeffdata <- cbind(outeffdata,MILD_rehearsal_min=mildlength_vals)
# rename them too
colnames(outeffdata) <- gsub("X","DLQ",colnames(outeffdata))

outeffdata = round(outeffdata,digits=3)
efffname <- paste(derivdir,"adherence-stats.csv",sep="/")
write.table(outeffdata,file=efffname,row.names=FALSE,col.names=TRUE,sep=",")
