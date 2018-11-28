import pandas as pd
import numpy as np
import pickle

def player_stat(name1, name2, df):
    player1 = (df.loc[df['player'] == name1]) 
    player2 = (df.loc[df['player'] == name2])
    both = pd.merge(player1,player2, how = 'outer')
    both = both.T
    both.reset_index(level=0, inplace=True)
    both.columns = both.iloc[0]
    stats = both.reindex(both.index.drop(0))
    stats = stats.rename(columns={'player':' '})
    stats = stats.set_index(' ')
    stats = stats.drop(['shots_made', '2pt_made', '3pt_made', 'FT_made'])
    return stats
