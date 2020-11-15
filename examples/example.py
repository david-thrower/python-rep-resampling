from resamples import mc_samples
import pandas as pd
import matplotlib.pyplot as plt

df = pd.DataFrame([[1,2],[3,4],[5,6],[7,8],[9,10]])
df.columns = ['a','b']

our_samples = mc_samples(df = df,n = 1000,reps = 1000,replace = True)
sample_means = our_samples.mean()

sample_means['a'].plot.density()
x1 = sample_means['a'].mean() + sample_means['a'].std()
plt.axvline(x=x1,color = 'y')
x2 = sample_means['a'].mean() - (sample_means['a'].std())
plt.axvline(x2,color = 'y')
x3 = sample_means['a'].mean() + 2 * sample_means['a'].std()
plt.axvline(x=x3,color='r')
x4 = sample_means['a'].mean() -(2 * (sample_means['a'].std()))
plt.axvline(x = x4,color='r')
plt.show()
# See the image example_output.png
