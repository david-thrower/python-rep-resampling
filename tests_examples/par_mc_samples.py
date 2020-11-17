from resamples import par_mc_samples
import dask
from dask import dataframe as dd
import pandas as pd
import matplotlib.pyplot as plt

df = dd.from_pandas(pd.DataFrame([[0,1],[2,3],[4,5],[6,7],[8,9]]),chunksize = 100)
#df = pd.DataFrame([[0,1],[2,3],[4,5],[6,7],[8,9]])
df.columns = ['a','b']
type(df) == dask.dataframe.core.DataFrame
# I know that the chnnksize I chose is > the size of the job. I am testing that the default of 100
# won't break something if a user submits a job smaller than 100. Maybe I am being OCD as usual.

samples = par_mc_samples(df = df, n = 1000,reps = 250, replace = True)
print('success')

a_sample_means = samples['a'].mean().compute()

standard_error_hat = a_sample_means.std()
mean_of_sample_means = a_sample_means.mean()
plt.axvline(mean_of_sample_means + standard_error_hat,color='y')
plt.axvline(mean_of_sample_means - standard_error_hat,color='y')
plt.axvline(mean_of_sample_means + 2 * standard_error_hat,color='r')
plt.axvline(mean_of_sample_means - 2 * standard_error_hat,color='r')

original_sample_mean = df['a'].mean().compute()
plt.axvline(original_sample_mean, color = 'g')

a_sample_means.plot.density()
plt.show()
a_sample_means.shape
