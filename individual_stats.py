import numpy as np
import pandas as pd
import random


#converting object to int64
#also adding -1 for rebounds
#col is points
def object_to_int(df, col):
    df['game_id'] = df['game_id'].astype('object')
    #df = df.convert_objects(convert_numeric=True)
    
    df['points'].replace(to_replace='', value= -1, inplace=True)
    df['2fg_attempts'] = df['2fg_attempts'].astype(np.int64)
    df['3pt_shots'] = df['3pt_shots'].astype(np.int64)
    df['med/hard_attempts'] = df['med/hard_attempts'].astype(np.int64)
    df = df.drop(['period',	'away_score', 'home_score', 'pts_difference', 'data_set',	'date',	'remaining_time','team','event_type'], axis = 1)
    
    return df


#make a df for assists, and one for blocks and one for the stats we got above
def assist_stats(df):
    ast = df.groupby('assist').sum()
    ast.reset_index(level=0, inplace=True)
    ast = ast.rename(columns={'assist':'player'})
    ast = ast.drop(['points','shots_made', 'FT_made', 'FT_missed', 'off_rebound','total_rebound', 'shots_missed', 'total_blocks', '3pt', '3pt_shots', 'Dunk/Layup', '2pt_med/hard', '2fg_attempts', 'Dunk/Layup_attempts', 'med/hard_attempts'], axis =1)
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
    df['APG'] = round(df['assist_count']/(df['total_games']), 2)
    df['BPG'] = round(df['total_blocks']/(df['total_games']), 2) 
    df['ORPG'] = round(df['off_rebound']/(df['total_games'] ), 2)
    df['RPG'] = round(df['total_rebound']/(df['total_games']), 2)
    
    df['easy_shot%'] = round((df['Dunk/Layup'] / df['Dunk/Layup_attempts']*100),1)
    df['2pt%'] = round((df['2pt_fg_made'] / df['2fg_attempts']*100),1)
    df['3pt%'] = round((df['3pt'] / df['3pt_shots']* 100),1)
    df['med/hard_fg%'] = round((df['2pt_med/hard'] / df['med/hard_attempts'] *100),1)
    
    return df



#USE THIS FOR RANDOM IDS

def add_ids(df):
    x = df.groupby('player').count().reset_index()
    x = x[['player']]
    x['player_id'] = [random.randint(1,10000000) for k in x.index]
    return x


# give ids to new players
def new_id(df, col):
    for value in df[col].values:
        if value!= 0:
            pass
        else:
            df[col] = [random.randint(1,10000000) for k in df.index]
    return df



#df2 = ids_df
#merge ids with all dfs
def merge_ids(df,df2):
    new_df = pd.merge(df2, df, on='player', how='outer')
    x_df = new_df[new_df['total_games']>=1]
    x_df = new_df[new_df['total_shots']>=1]
    x_df = x_df.fillna(0)
    #turn floats into int64 for columns that are not %
    lst = ['player_id','total_games','shots_made', 'shots_missed','3pt', '3pt_shots',	'Dunk/Layup','Dunk/Layup_attempts', '2pt_med/hard', 'med/hard_attempts', '2fg_attempts', 'FT_made', 'FT_missed', 'assist_count', 'off_rebound', 'total_rebound', 'total_blocks', '2pt_fg_made', 'total_shots']
    for y in lst:
        x_df[y] = x_df[y].astype(np.int64)
    return x_df


#df = df you gonna use to find turnovers
#and the new_df is a df with plyer names and total turnovers
def add_turnovers(df):
    df['pts_difference'] = df['away_score'] - df['home_score']
    df = pc.clutch_moment(df)
    x = df.groupby('player').count()
    new_df = x[['event_type']]
    new_df.reset_index(level=0, inplace=True)
    new_df = turnover_data.rename(columns={'event_type':'total_turnovers'})
    return new_df


def merge_turnovers(df,new_df):
    df = pd.merge(df,new_df,on='player', how = 'left')
    df = df.fillna(0)
    df['TPG'] = round(df['total_turnovers'] / df['total_games'],2)
    
    return new_df  
    
    

def add_league_avg(df):
    df = df.fillna(0)
    df['league_all_shot_avg'] = round((df['shots_made'].sum())/(df['total_shots'].sum())*100,1)
    df['league_2pt_avg'] = round((df['2pt_fg_made'].sum())/(df['2fg_attempts'].sum())*100,1)
    df['league_3pt_avg'] = round((df['3pt'].sum())/(df['3pt_shots'].sum())*100,1)
    df['league_hard2pt_avg'] = round((df['2pt_med/hard'].sum())/(df['med/hard_attempts'].sum())*100,1)
    df['league_easy2pt_avg'] = round((df['Dunk/Layup'].sum())/(df['Dunk/Layup_attempts'].sum())*100,1)
    df['league_ft%'] = round((df['FT_made'].sum()/ (df['FT_made'].sum() + df['FT_missed'].sum())*100), 1)
    
    return df


#assign weights to each type of shot
def add_scores(df):
    df['3pt_score'] = (df['3pt']*4)/(df['3pt_shots']*2)
    df['Hard_2Score'] = (df['2pt_med/hard']*3)/(df['med/hard_attempts']*2)
    df['Easy_2Score'] = (df['Dunk/Layup']*2)/(df['Dunk/Layup_attempts']*2)
    df['FT_score'] = (df['FT_made'])/(df['FT_made'] + df['FT_missed'])
    df = df.fillna(0)
    return df
        
    
def is_clutch(df):
    df['3pt_score'] = df['3pt_score'] * ((df['3pt_shots']>4)*1)
    df['Hard_2Score'] = df['Hard_2Score'] * ((df['2fg_attempts']>4)*1)
    df['Easy_2Score'] = df['Easy_2Score'] * ((df['2fg_attempts']>4)*1)
    df['FT_score'] = df['FT_score'] * (((df['FT_made'] + df['FT_missed'])>4)*1)
    df['total_score'] = df['3pt_score'] + df['Hard_2Score'] + df['Easy_2Score'] + df['FT_score'] - df['TPG']
    df['clutch_score'] = df['total_score']/4
    df['is_clutch'] = ((df['clutch_score'] > df['clutch_score'].mean()) & (df['total_shots']>round(df['total_shots'].mean())) & (df['shooting%'] > df['league_all_shot_avg']))*1
    return df


#only for final_test
def change_objects(df):
    df['game_id'] = df['game_id'].astype('object')
    #df = df.convert_objects(convert_numeric=True)
    
    df['points'].replace(to_replace='', value= -1, inplace=True)
    df['2fg_attempts'] = df['2fg_attempts'].astype(np.int64)
    df['3pt_shots'] = df['3pt_shots'].astype(np.int64)
    df['med/hard_attempts'] = df['med/hard_attempts'].astype(np.int64)
    df = df.drop(['period',	'away_score', 'home_score', 'pts_difference', 'data_set',	'date',	'remaining_time','team','event_type'], axis = 1)
    return df
    
    
    
