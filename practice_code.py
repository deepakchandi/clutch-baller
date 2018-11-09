import pandas as pd
import numpy as np


#adding new column
def add_pts(df):
    df['pts_difference'] = df['away_score']-df['home_score']
    return df


#removing columns
col_to_remove = (['a1', 'a2', 'a3','a4','a5','h1','h2','h3','h4','h5', 'play_length', 'entered', 'left', 'possession', 'shot_distance', 'original_x', 'original_y', 'converted_x', 'converted_y', 'num', 'away', 'home', 'outof', 'opponent', 'reason', 'elapsed', 'play_id'], axis = 1)
def remove_col(df, list_of_col):
    for items in list_of_col:
        df = df.drop([items], axis = 1)
    return df

#make df with only 2 min left in fourth quarter and overtime when the game is with in 5 pts
def clutch_moment(df):
 
    fourth_quarter = df[df['period']>=4]
    clutch = fouth_quarter[(fouth_quarter['remaining_time'] < '00:02:00') | (fouth_quarter['period']>4)]
    clutch_time = clutch[clutch['pts_difference']>=-5]
    clutch_time = clutch_time[clutch_time['pts_difference']<=5]
    return clutch_time


#removing unnecessary rows
#rows to remove contain these values:

rows = ['sub', 'timeout', 'uknown', 'unknown', 'Ejection', 'violat', 'traveling', 'team reb', 'foul',
        'turnover', 'of period', 'lost ball', 'goaltend', 'bad pass', 'illegal', 'jump ball', 'o']

def remove_junk_rows(df, column, list_of_rows):
    
    for item in list_of_rows:
        if item == 'o':
            df = df[df[column] != 'o']
        else:
            df=df[~df[column].str.contains(item)]
    return df 
          
#code for one specific row
#clutch_time = clutch_time[~clutch_time['type'].str.contains('sub')]              



#Changes the 'free throw #' with only 'free throw', make rebounds as just rebounds and changes all the shot types to just shot
f = []
def change_name(df, column):
    values = df[column].values
    for value in values:
        if "Free" in value:
            value = 'Free Throw'
        elif 'rebound' in value:
            value = 'rebound'
        else: # "Shot" or "Dunk" or "Layup" or "Roll" or 'Fadea' in value:
            value = 'Shot'
        f.append(value)
        
        
        
#gives you the shooting percent
def get_percent(df, column1, column2, name):
    a = df[(df[column1]==name) & ((df[column2]== 'miss')|(df[column2]=='shot'))][[column1, column2]]
    percent = np.sum(a[column2]=='shot')/a[column2].count()
    return percent


