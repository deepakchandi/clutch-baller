import numpy as np
import pandas as pd



#converting object to int64
#also adding -1 for rebounds
#col is points
def object_to_int(df, col):
    new_df = df.convert_objects(convert_numeric=True)
    new_df[col] = new_df[col].fillna(-1).astype(np.int64)
    new_df = new_df.drop(['period',	'away_score', 'home_score', 'pts_difference', 'data_set',	'date',	'remaining_time','team','event_type'], axis = 1)
    return new_df



#make a df for assists, and one for blocks and one for the stats we got above
def assist_stats(df):
    ast = df.groupby('assist').sum()
    ast.reset_index(level=0, inplace=True)
    ast = ast.rename(columns={'assist':'player'})
    ast = ast.drop([ 'points','shots_made', 'FT_made', 'FT_missed', 'off_rebound','total_rebound', 'shots_missed', 'total_blocks', '3pt', '3pt_shots', 'Dunk/Layup', '2pt_med/hard', '2fg_attempts', 'Dunk/Layup_attempts', 'med/hard_attempts'], axis =1)
    return ast

def blk_stats(df):
    blk = df.groupby('block').sum()
    blk.reset_index(level=0, inplace=True)
    blk = blk.rename(columns={'block':'player'})
    blk = blk.drop(['points', 'shots_made',	'FT_made',	'FT_missed', 'off_rebound',	'total_rebound','shots_missed', 'assist_count', '3pt', '3pt_shots', 'Dunk/Layup', '2pt_med/hard', '2fg_attempts', 'Dunk/Layup_attempts', 'med/hard_attempts'], axis =1)
    return blk

def player_names(df):
    plr_name = df.groupby(['player']).sum()
    plr_name.reset_index(level=0, inplace=True)
    plr_name = plr_name.drop('points', axis = 1)
    plr_name = plr_name.drop(['assist_count', 'total_blocks'], axis = 1)
    return plr_name
    
def merge_all(names,blocks,assists, df):
    result = pd.merge(names,blocks, on='player', how = 'outer')
    result_1 = pd.merge(result, assists, on='player', how = 'outer')
    result_2 = result_1.fillna(0)
    result_2['player'] = result_2['player'].dropna()
    result_2 = result_2[['player','shots_made', 'shots_missed','3pt', '3pt_shots',	'Dunk/Layup','Dunk/Layup_attempts', '2pt_med/hard', 'med/hard_attempts', '2fg_attempts', 'FT_made', 'FT_missed', 'assist_count', 'off_rebound', 'total_rebound', 'total_blocks']]
    
    new_df = (df.groupby(['player', 'game_id']).count()).reset_index()
    new_df = (new_df.groupby('player').count()).reset_index()
    new_df = new_df[['player','game_id']]
    new_df = new_df.rename(columns={'game_id':'total_games'})
    new_df = pd.merge(new_df, result_2, on='player', how='outer')
    
    return new_df


#add APG, BPG, FT%, FG%, RPG
def get_per_game_stats(df):
        
    #how many total toatl 2 pointers they made
    df['2pt_fg_made'] = df['Dunk/Layup'] + df['2pt_med/hard']
    
    
    df['shots_made'] = (df['3pt'] + df['Dunk/Layup'] + df['2pt_med/hard'])
    
    
    df['total_shots'] = (df['shots_made'] + df['shots_missed'])
    df['shooting%'] = round((df['shots_made']/(df['shots_made'] + df['shots_missed'])*100), 1)
    df['FT%'] = round((df['FT_made']/(df['FT_made']+ df['FT_missed']) * 100),1)
    df['APG'] = round(df['assist_count']/(df['total_games']), 1)
    df['BPG'] = round(df['total_blocks']/(df['total_games']), 1) 
    df['ORPG'] = round(df['off_rebound']/(df['total_games'] ), 1)
    df['RPG'] = round(df['total_rebound']/(df['total_games']), 1)
    
    df['easy_shot%'] = round((df['Dunk/Layup'] / df['Dunk/Layup_attempts']*100),1)
    df['2pt%'] = round((df['2pt_fg_made'] / df['2fg_attempts']*100),1)
    df['3pt%'] = round((df['3pt'] / df['3pt_shots']* 100),1)
    df['med/hard_fg%'] = round((df['2pt_med/hard'] / df['med/hard_attempts'] *100),1)
    
    return df



def add_ids(df):
    x = df.groupby('player').count().reset_index()
    x = x[['player']]
    x = x.assign(id=(x ['player'] ).astype('category').cat.codes)
    return x

#df2 = ids_df
#merge ids with all dfs
def merge_ids(df,df2):
    new_df = pd.merge(df2, df, on='player', how='outer')
    x_df = new_df[new_df['total_games']>=1]
    x_df = new_df[new_df['total_shots']>=1]
    x_df = x_df.fillna(0)
    #turn floats into int64 for columns that are not %
    lst = ['total_games','shots_made', 'shots_missed','3pt', '3pt_shots',	'Dunk/Layup','Dunk/Layup_attempts', '2pt_med/hard', 'med/hard_attempts', '2fg_attempts', 'FT_made', 'FT_missed', 'assist_count', 'off_rebound', 'total_rebound', 'total_blocks', '2pt_fg_made', 'total_shots']
    for y in lst:
        x_df[y] = x_df[y].astype(np.int64)
    return x_df



def add_league_avg(df):
    df = df.fillna(0)
    df['league_all_shot_avg'] = round((df['shots_made'].sum())/(df['total_shots'].sum())*100,1)
    df['league_2pt_avg'] = round((df['2pt_fg_made'].sum())/(df['2fg_attempts'].sum())*100,1)
    df['league_3pt_avg'] = round((df['3pt'].sum())/(df['3pt_shots'].sum())*100,1)
    df['league_hard2pt_avg'] = round((df['2pt_med/hard'].sum())/(df['med/hard_attempts'].sum())*100,1)
    df['league_easy2pt_avg'] = round((df['Dunk/Layup'].sum())/(df['Dunk/Layup_attempts'].sum())*100,1)
    
    return df


def is_clutch(df):
    df = df[df['total_games']>82]
    df['clutch_all_shots'] = (df['shooting%'] > df['league_all_shot_avg']) & (df['total_shots']>50)
    df['clutch_2pt'] = (df['2pt%'] > df['league_2pt_avg']) & (df['2fg_attempts']>35)
    df['clutch_3pt'] = (df['3pt%'] > df['league_3pt_avg']) & (df['3pt_shots']>25)
    df['clutch_hard2'] = (df['med/hard_fg%'] > df['league_hard2pt_avg']) & (df['med/hard_attempts']>20)
    df['clutch_easy2'] = (df['easy_shot%'] > df['league_easy2pt_avg']) & (df['Dunk/Layup_attempts']>20)
    return df
