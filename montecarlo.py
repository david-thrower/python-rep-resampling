def mc_samples(df,n,reps,replace = False,random_state = 8675309):
    from copy import copy
    cols = copy(df.columns)
    cols = cols.insert(0,'rep')
    mc_samples_to_return = pd.DataFrame().reindex(columns= cols)
    for i in range(0,reps):
        selected_samples_for_rep = pd.DataFrame(df.sample(10,replace=replace,random_state=random_state))
        rep_number = []
        for j in range(0,n):
            rep_number.append([copy(i)])
        rep_number = pd.DataFrame(rep_number)
        rep_number.columns = ['rep_number']
        selected_samples_for_rep.reset_index(drop=True, inplace=True)
        selected_samples_for_rep = pd.concat((copy(rep_number),copy(selected_samples_for_rep)),axis = 1,ignore_index = True)
        selected_samples_for_rep.columns = cols
        mc_samples_to_return = pd.concat((copy(mc_samples_to_return),copy(selected_samples_for_rep)), axis = 0)
        random_state += 1
    mc_samples_to_return = mc_samples_to_return.groupby(by='rep')
    return mc_samples_to_return
