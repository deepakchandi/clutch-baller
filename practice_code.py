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
    df1 = df.replace(np.nan, '', regex=True)
    return df1


#removing columns
#col_to_remove = (['a1', 'a2', 'a3','a4','a5','h1','h2','h3','h4','h5', 'play_length', 'entered', 'left', 'possession', 'shot_distance', 'original_x', 'original_y', 'converted_x', 'converted_y', 'num', 'away', 'home', 'outof', 'opponent', 'reason', 'elapsed', 'play_id'], axis = 1)

def remove_col(df, list_of_col):
    for items in list_of_col:
        df = df.drop([items], axis = 1)
    return df


#removing unnecessary rows
#rows to remove contain these values:
#and add player id's

#rows = ['sub', 'timeout', 'uknown', 'unknown', 'Ejection', 'violat', 'traveling', 'team reb', 'foul', 'turnover', 'of period', 'lost ball', 'goaltend', 'bad pass', 'illegal', 'jump ball', 'o'] if col = 'type


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


#
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



#gives you the shooting percent
#for me column1 = 'player', column2='event_type', name = player you wanna see
def get_percent(df, name):
    a = df[(df['player']==name) & ((df['event_type']== 'miss')|(df['event_type']=='shot'))]
    percent = np.sum(a['event_type']=='shot')/a['event_type'].count()
    return ("Shooting Percentage:{}".format(round(percent, 3)),'Made: {}'.format(np.sum(a['event_type']=='shot')),
           'Attempt: {}'.format(a['event_type'].count()))


#gives yu the free throw numbers for a certain player
#for me column1 = 'player', column2='event_type', column3= 'result' name = player you wanna see
def free_throw_percent(df,name):
    a = df[(df['player']==name) & (df['event_type'] == 'free throw') & ((df['result']== 'made')|
                                        (df['result']=='missed'))]
    percent = np.sum(a['result']=='made')/a['result'].count()
    return("Free Throw:{}".format(round(percent, 3)),'Made: {}'.format(np.sum(a['result']=='made')),
           'Attempt: {}'.format(a['result'].count()))




#compare two players shooting stats:
def compare_stats(df, name1, name2):

    a = df[(df['player']==name1) & ((df['event_type']== 'miss')|(df['event_type']=='shot'))]
    percent1 = np.sum(a['event_type']=='shot')/a['event_type'].count()

    b = df[(df['player']==name2) & ((df['event_type']== 'miss')|(df['event_type']=='shot'))]
    percent2 = np.sum(b['event_type']=='shot')/b['event_type'].count()

    return ('Player A:{}'.format(name1), "Shooting Percentage:{}".format(round(percent1, 3)),'Made: {}'.format(np.sum(a['event_type']=='shot')),
            'Attempt: {}'.format(a['event_type'].count()),
            'Player B:{}'.format(name2), "Shooting Percentage:{}".format(round(percent2, 3)),'Made: {}'.format(np.sum(b['event_type']=='shot')),
            'Attempt: {}'.format(b['event_type'].count())
           )


#compare shooting and free throw stats
def compare_players(df, name1, name2):

    a1 = df[(df['player']==name1) & ((df['event_type']== 'miss')|(df['event_type']=='shot'))]
    a2 = df[(df['player']==name1) & (df['event_type'] == 'free throw') & ((df['result']== 'made')| (df['result']=='missed'))]

    percenta1 = np.sum(a1['event_type']=='shot')/a1['event_type'].count()
    percenta2 = np.sum(a2['result']=='made')/a2['result'].count()

    b1 = df[(df['player']==name2) & ((df['event_type']== 'miss')|(df['event_type']=='shot'))]
    b2 = df[(df['player']==name2) & (df['event_type'] == 'free throw') & ((df['result']== 'made')|(df['result']=='missed'))]

    percentb1 = np.sum(b1['event_type']=='shot')/b1['event_type'].count()
    percentb2 = np.sum(b2['result']=='made')/b2['result'].count()

    s = ((' ', 'Shooting Percentage', 'Shots Made', 'Shots Attempted', 'FT Percentage', 'FT Made','FT Attempts'),(name1, (round(percenta1, 3)),(np.sum(a1['event_type']=='shot')),
            (a1['event_type'].count()), (round(percenta2, 3)),(np.sum(a2['result']=='made')),
           (a2['result'].count())),
            (name2, (round(percentb1, 3)),(np.sum(b1['event_type']=='shot')),
            (b1['event_type'].count()), (round(percentb2, 3)),(np.sum(b2['result']=='made')),
           (b2['result'].count())))
    
    g = pd.DataFrame(list(s)).T
    g.columns = g.iloc[0]
    g.drop(0, inplace=True)
    g = g.set_index(' ')
    return g

    
    
    

#groupby all the close games by player name and then give you how many games each player played
#col1: player and col2:game_id
def get_total_games(df):
    new_df = (df.groupby(['player', 'game_id']).count()).reset_index()
    new_df = (new_df.groupby('player').count()).reset_index()
    new_df = new_df[['player','game_id']]
    new_df = new_df.rename(columns={'game_id':'total_games'})
    return new_df












#USE THE SAME CODE FOR ASSISTS, AND BLOCKS AS WELL

#col1:off_rebound, col2:player, col3:game_id

def get_intangibles(df, col):
    if col == 'off_rebound':
        intangible = df[df['type']=='rebound offensive']
    if col == 'assist':
        intangible = df[df['assist']!='']
    if col == 'block':
        intangible = df[df['block']!='']
        
    return intangible
    
#gives all the offenvie rebound stats    
def off_rebounds_in_clutch(df, col1, col2, col3):
            
    intangible_feature = get_intangibles(df,col1)
    
    intangible_dic={}
    for value in intangible_feature[col2].values:
        if value not in intangible_dic.keys():
            intangible_dic[value]=1
        else:
            intangible_dic[value]+=1
            
    if col1 == 'off_rebound':            
        rebound_per_player = pd.DataFrame.from_dict(intangible_dic,orient = 'index')
        rebound_per_player = rebound_per_player.reset_index()
        rebound_per_player = rebound_per_player.rename(columns={'index':'player', 0:'total_rebound'})

        total_games = get_total_games(df, col2,col3)

    #merge two df so we get total games played and total offensive rebounds for each player
        off_rebounds = total_games.merge(rebound_per_player, on = 'player')

    #create a new column with off_rebund per game
        off_rebounds['off_rebound/clutch time']=off_rebounds.apply(lambda row: row.total_rebound / row.clutch_games, axis = 1)

        clutch_rebounds = off_rebounds.sort_values(by = ['total_rebound', 'clutch_games'], ascending=False)

    return clutch_rebounds
        
        
        
def assits_per_game(df, col1, col2, col3):
    
    intangible_feature = get_intangibles(df,col1)

    assist_dic= {}
    for value in intangible_feature[col1].values:
        if value not in assist_dic.keys():
            assist_dic[value]=1
        else:
            assist_dic[value]+=1

    #counts how many rebounds each player has in total
    assist_per_player = pd.DataFrame.from_dict(assist_dic,orient = 'index')
    assist_per_player = assist_per_player.reset_index()
    assist_per_player = assist_per_player.rename(columns={'index':'player', 0:'total_assist'})

    total_games = get_total_games(df, col2, col3)

    l = total_games.merge(assist_per_player, on = col2)

    #create a new column with assists per game

    l['assist_per_clutch_time']=l.apply(lambda row: row.total_assist / row.clutch_games, axis =1)

    #sorted by amount of games and assists

    l = l.sort_values(by = ['player','total_assist', 'clutch_games'])
    
    return round(l, 3)



#code to get blocks:

def get_all_blocks(df, col1, col2, col3):
    
    intangible_feature = get_intangibles(df,col1)
    
    blk_dic= {}
    for value in intangible_feature[col1].values:
        if value not in blk_dic.keys():
            blk_dic[value]=1
        else:
            blk_dic[value]+=1

    blocks_1 = pd.DataFrame.from_dict(blk_dic,orient = 'index')
    blocks_1 = blocks_1.reset_index()
    blocks_1 = blocks_1.rename(columns={'index':'player', 0:'total_blocks'})

    total_games = get_total_games(df, col2, col3)

    l = total_games.merge(blocks_1, on = col2)

    #create a new column with assists per game

    l['block_per_clutch_time']=l.apply(lambda row: row.total_blocks / row.clutch_games, axis =1)

    #sorted by amount of games and assists

    l = l.sort_values(by = ['player','total_blocks', 'clutch_games'])
    
    return round(l, 3)









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
