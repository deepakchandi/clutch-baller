import numpy as np
import pandas as pd



#adding new columns:
#adds a pts differnce column
#adds a column that shows who won atht game
#add player_id
def add_columns(df):
    df['pts_difference'] = df['away_score']-df['home_score']
    
    df2 = df[((df['event_type']=='end of period') & (df['period']>=4) & (df['pts_difference']!=0))]
    df2['winner'] = np.where(df2.pts_difference >0, 'away', 'home')
    new_df = pd.merge(df,df2[['game_id','winner']],on='game_id', how='left')
    new_df['shots_missed'] = (new_df['event_type']=='miss')*1
    new_df['total_rebound'] = (new_df['event_type']=='rebound')*1
    new_df['FT_made'] = ((new_df['event_type']=='free throw') & (new_df['result']=='made'))*1
    new_df['off_rebound'] = ((new_df['event_type']=='rebound') & (new_df['type']=='rebound offensive'))*1
    new_df['FT_missed'] = ((new_df['event_type']=='free throw') & (new_df['result']=='missed'))*1
    new_df['total_blocks'] = (new_df['block']!='')*1
    new_df['assist_count'] = (new_df['assist']!='')*1
    
    
    new_df['shots_made'] = (new_df['event_type']=='shot')*1
    
    ##points made/ attempted
    new_df['3pt'] = (new_df['points'] == 3)*1
    
    new_df['3pt_shots'] = new_df['description'].str.contains('3PT')*1
    
    #how many easy shots they made
    new_df['Dunk/Layup'] = ((new_df['points'] == 2) & ((new_df['type'].str.contains('Layup')) | (new_df['type'].str.contains('Dunk')) | new_df['type'].str.contains('Finger Roll'))) *1
    
    new_df['Dunk/Layup_attempts'] = ((new_df['type'].str.contains('Layup') | new_df['type'].str.contains('Dunk') | new_df['type'].str.contains('Finger Roll')))*1
        
    
    #how many not easy 2pointers they made
    new_df['2pt_med/hard'] = ((new_df['type'].str.contains('Fadeaway') & (new_df['points'] == 2))| (new_df['type'].str.contains('Shot')  & (new_df['points'] == 2)))*1
    
    new_df['med/hard_attempts'] = (((new_df['points'] != 3) & new_df['type'].str.contains('Shot') | (new_df['points'] != 3) & new_df['type'].str.contains('Fadeaway'))*1)- (new_df['3pt_shots'] - new_df['3pt'])
    

    #how many 2pt fg attempted
    new_df['2fg_attempts'] = (new_df['shots_made'] + new_df['shots_missed']) - new_df['3pt_shots']
    
    return new_df



def replace_nan(df):
    df = df.replace(np.nan, '', regex=True)
    return df


#removing columns
#col_to_remove = ['a1', 'a2', 'a3','a4','a5','h1','h2','h3','h4','h5', 'play_length', 'entered', 'left', 'possession', 'shot_distance', 'original_x', 'original_y', 'converted_x', 'converted_y', 'num', 'away', 'home', 'outof', 'opponent', 'reason', 'elapsed', 'play_id']

def remove_col(df, list_of_col):
    for items in list_of_col:
        df = df.drop([items], axis = 1)
    return df


#removing unnecessary rows
#rows to remove contain these values:
#and add player id's

#if col is 'event_type'
#rows = ['timeout', 'sub', 'ejection', 'violation', 'turnover', 'foul', 'jump ball' ]

def remove_junk_rows(df, column):
    rows = ['timeout', 'sub', 'ejection', 'violation', 'turnover', 'foul', 'jump ball', 'of period', 'unknown' ]
    rows1= ['unknown', 'team rebo']
    for item in rows:
        df=df[~df[column].str.contains(item)]
    for i in rows1:
        df = df[~df['type'].str.contains(i)]
    return df


#code for one specific row
#clutch_time = clutch_time[~clutch_time['type'].str.contains('sub')]


#Separating playoffs from regular season
def regular_or_playoffs(df, col_to_use):
    regular_season = df[df[col_to_use].str.endswith('Season')]
    playoffs = df[df[col_to_use].str.endswith('Playoff')]
    return (regular_season, playoffs)


#make df with only 2 min left in fourth quarter and overtime when the game is with in 5 pts
def clutch_moment(df):

    clutch = df[df['period']>=4]
    clutch = clutch[(clutch['remaining_time'] < '00:02:00') | (clutch['period']>4)]
    clutch_time = clutch[clutch['pts_difference']>=-6]
    clutch_time = clutch_time[clutch_time['pts_difference']<=6]
    return clutch_time

#remove games that were mentioned only 9 times or less because they are not clutch:
# the column we use is game_id because that deferntiate between games
def remove_not_imp_games(df, column):
    df = df.groupby(column).filter(lambda x : len(x)>9)
    return df
    
    
    

#groupby all the close games by player name and then give you how many games each player played
#col1: player and col2:game_id
def get_total_games(df):
    new_df = (df.groupby(['player', 'game_id']).count()).reset_index()
    new_df = (new_df.groupby('player').count()).reset_index()
    new_df = new_df[['player','game_id']]
    new_df = new_df.rename(columns={'game_id':'total_games'})
    x = new_df.sort_values('total_games', ascending = False)
    return x


if __name__=="__main__":
    add_pts()
    remove_col()
    clutch_moment()
    remove_junk_rows()
    regular_or_playoffs()
    change_name()
    get_percent()
    free_throw_percent()
    compare_stats()
    compare_players()
