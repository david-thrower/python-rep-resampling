def mc_samples(df,n,reps,replace = False,random_state = 8675309):
    import pandas as pd
    from copy import copy
    cols = copy(df.columns)
    cols = cols.insert(0,'rep')
    mc_samples_to_return = pd.DataFrame().reindex(columns= cols)
    for i in range(0,reps):
        selected_samples_for_rep = pd.DataFrame(df.sample(n,replace=replace,random_state=random_state))
        rep_number = []
        for j in range(0,n):
            rep_number.append([copy(i)])
        rep_number = pd.DataFrame(rep_number)
        rep_number.columns = ['rep_number']
        selected_samples_for_rep.reset_index(drop=True, inplace=True)
        selected_samples_for_rep = pd.concat((copy(rep_number),copy(selected_samples_for_rep)),axis = 1,ignore_index = True,sort=False)
        selected_samples_for_rep.columns = cols
        mc_samples_to_return = pd.concat((copy(mc_samples_to_return),copy(selected_samples_for_rep)), axis = 0,sort=False)
        random_state += 1
    mc_samples_to_return = mc_samples_to_return.groupby(by='rep')
    return mc_samples_to_return

def par_mc_samples(df,n,reps,replace = False,random_state = 8675309, chunksize = 100):
    import dask
    import dask.dataframe as dd
    from copy import copy
    import pandas as pd
    cols = copy(df.columns)
    cols = cols.insert(0,'rep')
    mc_samples_to_return = dd.from_pandas(pd.DataFrame().reindex(columns= cols),chunksize=chunksize)
    if type(df) != dask.dataframe.core.DataFrame:
        dd_df = dd.from_pandas(df,chunksize = chunksize)
    else:
        dd_df = df
    for i in range(0,reps):
        frac = n/dd_df.shape[0].compute()
        selected_samples_for_rep = dd_df.sample(frac = frac,replace=replace,random_state=random_state).compute()
        rep_number = []
        for j in range(0,n):
            rep_number.append([copy(i)])
        rep_number = dd.from_pandas(pd.DataFrame(rep_number),chunksize=chunksize)
        rep_number.columns = ['rep_number']
        selected_samples_for_rep.reset_index(drop=True, inplace=True)
        selected_samples_for_rep = dd.from_pandas(selected_samples_for_rep,chunksize = chunksize)
        selected_samples_for_rep = dd.concat([copy(rep_number),copy(selected_samples_for_rep)],axis = 1,ignore_index = True,sort = False)
        selected_samples_for_rep.columns = cols
        mc_samples_to_return = dd.concat([copy(mc_samples_to_return),copy(selected_samples_for_rep)], axis = 0,sort=False)
        random_state += 1
    mc_samples_to_return = mc_samples_to_return.groupby(by='rep')
    return mc_samples_to_return
