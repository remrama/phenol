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


####  parameter setup  ####

p <- fromJSON(file='./config.json')
DATA_DIR  <- p$data_directory
DERIV_DIR <- p$derivatives_directory

IMPORT_FNAME <- paste(DATA_DIR,"data.csv",sep="/")

EXPORT_FNAME_1 <- paste(DERIV_DIR,"adherence-coefficients.csv",sep="/")
EXPORT_FNAME_2 <- paste(DERIV_DIR,"adherence-stats.csv",sep="/")

###########################


####  load data  ####

data <- read.csv(IMPORT_FNAME,na.strings="NA")
# only use those rows with dream recall
data = data[!is.na(data$dream_report),]

# make sure factors are factors
data$participant_id <- factor(data$participant_id)
data$DLQ_01 <- factor(data$DLQ_01,ordered=TRUE)

#######################


####  run regression  ####

# build ordinal regression
model.fit <- clmm(DLQ_01 ~ (1|participant_id)
    + n_reality_checks + MILD_rehearsal_min + MILD_awake_min,
    data=data)

# run regression
print(summary(model.fit))

# get odds ratios by taking exponent of the coefficients
# (makes coeffs interpretable)
outdf <- exp(cbind(OddsRatio=coef(model.fit),confint(model.fit)))

#######################


####  reorganize and export  ####

# add pvalue from regression model to this dataframe
outdf <- cbind(outdf,pval=summary(model.fit)$coefficients[,"Pr(>|z|)"])

# drop the useless stuff from dataframe
predictors = c("n_reality_checks","MILD_rehearsal_min","MILD_awake_min")
outdf <- outdf[predictors,]

# export
outdf = round(outdf,digits=3)
write.table(outdf,file=EXPORT_FNAME_1,row.names=TRUE,col.names=NA,sep=",")

#######################

####  export model predictions for plotting in python ####

mildlength_vals <- 0:20
effdata <- Effect(focal.predictors=c("MILD_rehearsal_min"),mod=model.fit,
                  xlevels=list(MILD_rehearsal_min=mildlength_vals))

outeffdata <- effdata["prob"]$prob

# add col denoting mildlength used for model prediction
outeffdata <- cbind(outeffdata,MILD_rehearsal_min=mildlength_vals)

# rename them too
colnames(outeffdata) <- gsub("X","DLQ",colnames(outeffdata))

outeffdata = round(outeffdata,digits=3)
write.table(outeffdata,file=EXPORT_FNAME_2,row.names=FALSE,col.names=TRUE,sep=",")

#######################
