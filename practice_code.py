import pandas as pd
import numpy as np


pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)



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
    clutch_time = clutch[clutch['pts_difference']>=-6]
    clutch_time = clutch_time[clutch_time['pts_difference']<=6]
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



#Separating playoffs from regular season
def regular_or_playoffs(df, col_to_use):
    regular_season = df[df[col_to_use].str.endswith('Season')]
    playoffs = df[df[col_to_use].str.endswith('Playoff')]
    return (regular_season, playoffs)                   



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
    a = df[(df[column1]==name) & ((df[column2]== 'miss')|(df[column2]=='shot'))]
    percent = np.sum(a[column2]=='shot')/a[column2].count()
    return ("Shooting Percentage:{}".format(round(percent, 3)),'Made: {}'.format(np.sum(a[column2]=='shot')), 
           'Attempt: {}'.format(a[column2].count()))

#gives yu the free throw numbers for a certain player
def free_throw_percent(df, column1, column2, column3,  name):
    a = df[(df[column1]==name) & (df[column2] == 'free throw') & ((df[column3]== 'made')|
                                        (df[column3]=='missed'))][[column1, column2, column3]]
    percent = np.sum(a[column3]=='made')/a[column3].count()
    return("Free Throw:{}".format(round(percent, 3)),'Made: {}'.format(np.sum(a[column3]=='made')), 
           'Attempt: {}'.format(a[column3].count()))




#compare two players shooting stats:
def compare_stats(df, column1, column2, name1, name2):
   
    a = df[(df[column1]==name1) & ((df[column2]== 'miss')|(df[column2]=='shot'))]
    percent1 = np.sum(a[column2]=='shot')/a[column2].count()
    
    b = df[(df[column1]==name2) & ((df[column2]== 'miss')|(df[column2]=='shot'))]
    percent2 = np.sum(b[column2]=='shot')/b[column2].count()
    
    return ('Player A:{}'.format(name1), "Shooting Percentage:{}".format(round(percent1, 3)),'Made: {}'.format(np.sum(a[column2]=='shot')), 
            'Attempt: {}'.format(a[column2].count()),
            'Player B:{}'.format(name2), "Shooting Percentage:{}".format(round(percent2, 3)),'Made: {}'.format(np.sum(b[column2]=='shot')), 
            'Attempt: {}'.format(b[column2].count())
           )


#compare shooting and free throw stats
def compare_players(df, column1, column2, column3, name1, name2):
    
    a1 = df[(df[column1]==name1) & ((df[column2]== 'miss')|(df[column2]=='shot'))]
    a2 = df[(df[column1]==name1) & (df[column2] == 'free throw') & ((df[column3]== 'made')|
                                        (df[column3]=='missed'))]
    
    percenta1 = np.sum(a1[column2]=='shot')/a1[column2].count()
    percenta2 = np.sum(a2[column3]=='made')/a2[column3].count()
    
    b1 = df[(df[column1]==name2) & ((df[column2]== 'miss')|(df[column2]=='shot'))]
    b2 = df[(df[column1]==name2) & (df[column2] == 'free throw') & ((df[column3]== 'made')|
                                        (df[column3]=='missed'))]
    
    percentb1 = np.sum(b1[column2]=='shot')/b1[column2].count()
    percentb2 = np.sum(b2[column3]=='made')/b2[column3].count()    


    return(('Player A:{}'.format(name1), "Shooting Percentage:{}".format(round(percenta1, 3)),'Made: {}'.format(np.sum(a1[column2]=='shot')), 
            'Attempt: {}'.format(a1[column2].count()), "Free Throw:{}".format(round(percenta2, 3)),'Made: {}'.format(np.sum(a2[column3]=='made')), 
           'Attempt: {}'.format(a2[column3].count())),
            ('Player B:{}'.format(name2), "Shooting Percentage:{}".format(round(percentb1, 3)),'Made: {}'.format(np.sum(b1[column2]=='shot')), 
            'Attempt: {}'.format(b1[column2].count()), "Free Throw:{}".format(round(percentb2, 3)),'Made: {}'.format(np.sum(b2[column3]=='made')), 
           'Attempt: {}'.format(b2[column3].count())))