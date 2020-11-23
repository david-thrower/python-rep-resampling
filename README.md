# Module resamples

Purpose: Provides a way to resample a pandas data frame or dask dataframe into a
set of replicate samples which simulate the sampling distribution. This is done
in one line of code and returns a dataframe grouped by replicate 'rep':

## methods

### mc_samples(df,n,reps,replace = False,random_state = 8675309)

**Note:** This method is recommended for smaller resamplings on a single machine, on
a single core. Generally I recommend to create no more than 50,000 rows per few GB of memory
and per 4 cores you have. In no case would it make sense to use this to create a total of more than
100,000 rows. Use the method par_mc_samples instead. This is below.  

**Paramters**
df: Any Pandas DataFrame object WITH NAMED COLUMNS If the columns in your
DataFrame are not named, you will get:
"TypeError: assign() keywords must be strings". To fix this, name your columns:
df_name.columns = ['column_1_name',column_2_name ... column_n_name]   
**n:** int: number of observations drawn per replicate   
**reps:** int: Number of replicates   
**replace:** Boolean: Whether a row that is selected can be selected again. If you are
creating replicates that are larger than the original sample size, then this
must be set to True.   
**random_state:** The seed for the random number generator. This is used to make results reproducible by uniformity in the psuedo quasi random numbers selected in sampling.  

**Returns:** pandas.core.groupby.generic.DataFrameGroupBy (grouped by replicate 'rep')

When you call the method resampled_df_name['column_name'].mean(),
it will return a list of each of the sample mean for the chosen column for each replicate.
You can plot a density plot of the sample distribution by calling resampled_df_name['column_name'].mean().plot.density(). Calling resampled_df_name['column_name'].mean().std() will return the simulated / estimated standard error for the selected column's mean, and resampled_df_name['column_name'].mean().mean().compute() will return the mean of the sampling distribution. Of course, from there, you have the sample mean of your original real sample, the mean of the sample distribution, and the estimated standard error, so you derive the statistics you are looking for from there such as CI and p(mean > [x])...


### def par_mc_samples(df,n,reps,replace = False,random_state = 8675309, chunksize = 100):

**Paramters**
df: Any Pandas DataFrame object WITH NAMED COLUMNS or any  If the columns in your
DataFrame are not named, you will get:
"TypeError: assign() keywords must be strings". To fix this, name your columns:
df_name.columns = ['column_1_name',column_2_name ... column_n_name]   
**n:** int: number of observations drawn per replicate   
**reps:** int: Number of replicates   
**replace:** Boolean: Whether a row that is selected can be selected again. If you are
creating replicates that are larger than the original sample size, then this
must be set to True.   
**random_state:** The seed for the random number generator. This is used to make results reproducible by uniformity in the psuedo quasi random numbers selected in sampling.  
chunksize = The number of records that will be run at a time in each parallel operation   

**Returns:** dask.dataframe.groupby.DataFrameGroupBy (grouped by replicate 'rep')

A dask dataframe behaves like a Pandas DataFrame, but it operates in a
parallelized manner. For a simple example: When you call the method resampled_df_name['column_name'].mean().compute(),
it will return a list of sample means for each replicate just like resampled_df_name['column_name'].mean() would in the Pandas version of the same. This can also be used to plot a density plot of the sample distribution by calling resampled_df_name['column_name'].mean().compute().plot.density(). Calling resampled_df_name['column_name'].mean().std().compute() will return the estimated standard error for the selected column, and resampled_df_name['column_name'].mean().mean().compute() will return the mean of the sampling distribution. The math to compute these will all be performed in parallel in chunks of 100 rows by default or whatever you set the argument chunksize to. The reason for the extra method.compute() after everything here is because this operates on futures parallelization. Of course, from there, you have the sample mean, the mean of the sample distribution, and the standard error, so you derive the statistics you are looking for from there.

**Note:** This method is recommended for creating large resamplings. If
you are creating more around 50,000 or 100,000 rows in total, this is probably for you and
may be by far your most efficient option in this package.

## Example:  
from resamples import par_mc_samples  
import pandas as pd  
import matplotlib.pyplot as plt  
import scipy.stats as st  

df = pd.DataFrame([[1,2],[3,2],[5,6],[7,7],[9,0]])  
df.columns = ['a','b']  

original_sample_means = df.mean()  


pooled_sample = pd.DataFrame({'pooled_a_b':pd.concat([df['a'],df['b']],axis=0)})  


resampled_pooled_df = par_mc_samples(pooled_sample,10,1000,replace = True)  
resampled_means_for_each_rep = resampled_pooled_df.mean().compute()  
sample_distribution_mean = resampled_pooled_df.mean().mean().compute()  

std_error = resampled_pooled_df.mean().std().compute()  

resampled_pooled_df.mean().compute().plot.density(color = 'aqua')  

#plt.axvline(original_sample_means['a'],color = 'fuchsia')  
#plt.axvline(original_sample_means['b'],color = 'mediumvioletred')  
# Sample distribution mean  
plt.axvline(sample_distribution_mean[0],color = 'aqua')  
# Difference of the means of sample a and sample b divided by the standard error (scaled to the sampling distribution mean)  
scaled_std_errors_difference_a_b = sample_distribution_mean[0] + (original_sample_means['a'] - original_sample_means['b'])/std_error[0]  
plt.axvline(scaled_std_errors_difference_a_b,color = 'green')  


plt.axvline(sample_distribution_mean[0] + 1.65 * std_error[0],color='r')  
#plt.axvline(sample_distribution_mean[0] - std_error[0],color='y')  
#plt.axvline(sample_distribution_mean[0] + 2 * std_error[0],color='r')  
#plt.axvline(sample_distribution_mean[0] - 2 * std_error[0],color='r')  

plt.show()  

print("We simulated the null distribution for the pooled populations reporesented by samples a and b")  
print("H0: The population mean of sample a <= the population mean of sample b")  
print("H1: The population mean of sample a > the population mean of sample b")  
print("There is sufficient evidence to reject the null hypothesis that a <= b and conclude that")  
print("the mean of sample a > the mean of sample b.")  
print(f"p = {1 - st.norm.cdf((original_sample_means['a'] - original_sample_means['b'])/std_error[0])}")  
