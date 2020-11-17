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
a = pd.DataFrame([[1,2],[3,4],[5,6],[7,8],[9,0]])
a.columns = ['a','b']
a_sample_mean = a['a'].mean()
res_a_par = par_mc_samples(a,10,1000,replace = True)
a_means = res_a_par['a'].mean().compute()
res_a_par['a'].mean().compute().plot.density()
a_std_error = res_a_par['a'].mean().std().compute()
a_sample_dist_mean = res_a_par['a'].mean().mean().compute()
plt.axvline(a_sample_mean,color = 'b')
plt.axvline(a_sample_dist_mean + a_std_error,color='y')
plt.axvline(a_sample_dist_mean - a_std_error,color='y')
plt.axvline(a_sample_dist_mean + 2 * a_std_error,color='r')
plt.axvline(a_sample_dist_mean - 2 * a_std_error,color='r')
plt.show()
