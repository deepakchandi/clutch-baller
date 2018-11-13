#functions for getting all the players stats as one df

import numpy as np
import pandas as pd



#converting object to int64
#also adding -1 for rebounds
#col is points
def object_to_int(df, col):
    new_df = df.convert_objects(convert_numeric=True)
    new_df[col] = new_df[col].fillna(-1).astype(np.int64)
    return new_df


#adding columns to count shots made, taken, rebounds, FT
#col is either event_type, type, result
def add_more_columns(df):
    new_df = df.copy()
    new_df['shots_made'] = (new_df['event_type']=='shot')*1
    new_df['shots_missed'] = (new_df['event_type']=='miss')*1
    new_df['total_rebound'] = (new_df['event_type']=='rebound')*1
    new_df['FT_made'] = ((new_df['event_type']=='free throw') & (new_df['result']=='made'))*1
    new_df['off_rebound'] = ((new_df['event_type']=='rebound') & (new_df['type']=='rebound offensive'))*1
    new_df['FT_missed'] = ((new_df['event_type']=='free throw') & (new_df['result']=='missed'))*1
    new_df['total_blocks'] = (new_df['block']!='')*1
    new_df['assist_count'] = (new_df['assist']!='')*1
    new_df = new_df.drop(['period',	'away_score', 'home_score', 'pts_difference', 'data_set',	'date',	'remaining_time',	'team',	'event_type'], axis = 1)
    return new_df


#make a df for assists, and one for blocks and one for the stats we got above
def combine_stats(df):
    ast = df.groupby('assist').sum()
    ast.reset_index(level=0, inplace=True)
    ast = ast.rename(columns={'assist':'player'})
    ast = ast.drop([ 'points','shots_made', 'FT_made', 'FT_missed', 'off_rebound','total_rebound', 'shots_missed', 'total_blocks'], axis =1)
    return ast

def blk_stats(df):
    blk = df.groupby('block').sum()
    blk.reset_index(level=0, inplace=True)
    blk = blk.rename(columns={'block':'player'})
    blk = blk.drop(['points', 'shots_made',	'FT_made',	'FT_missed', 'off_rebound',	'total_rebound',	'shots_missed', 'assist_count'], axis =1)
    return blk

def player_names(df):
    plr_name = df.groupby(['player']).sum()
    plr_name.reset_index(level=0, inplace=True)
    plr_name = plr_name.drop('points', axis = 1)
    return plr_name
    
def merge_all(a,b,c):   
    result = pd.merge(a, b, on='player', how = 'outer')
    #result_1 = pd.merge(result, c, on='player', how = 'outer')
    #result_2 = result_1.fillna(0)
    #result = result.drop(['period_x','away_score_x',	'home_score_x',	'points_x',	'pts_difference_x'],axis = 1) 
    return result
