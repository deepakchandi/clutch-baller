#All the codes for getting one player stats or comparing two players

#replace all the empty fields with string 'empty'
def replace_nan(df):
    df1 = df.replace(np.nan, '', regex=True)
    return df1



#adding new columns:
#adds a pts differnce column
#adds a column that shows who won atht game
def add_columns(df):
    df['pts_difference'] = df['away_score']-df['home_score']
    
    df2 = df[(df['event_type']=='end of period') & (df['period']>=4) & (df['pts_difference']!=0)]
    df2['winner'] = np.where(df2.pts_difference >0, 'away', 'home')
    new_df = pd.merge(df,df2[['game_id','winner']],on='game_id', how='left')
    return new_df


#removing columns
#col_to_remove = (['a1', 'a2', 'a3','a4','a5','h1','h2','h3','h4','h5', 'play_length', 'entered', 'left', 'possession', 'shot_distance', 'original_x', 'original_y', 'converted_x', 'converted_y', 'num', 'away', 'home', 'outof', 'opponent', 'reason', 'elapsed', 'play_id'], axis = 1)
def remove_col(df, list_of_col):
    for items in list_of_col:
        df = df.drop([items], axis = 1)
    return df

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



#gives you the shooting percent
#for me column1 = 'player', column2='event_type', name = player you wanna see
def get_percent(df, column1, column2, name):
    a = df[(df[column1]==name) & ((df[column2]== 'miss')|(df[column2]=='shot'))]
    percent = np.sum(a[column2]=='shot')/a[column2].count()
    return ("Shooting Percentage:{}".format(round(percent, 3)),'Made: {}'.format(np.sum(a[column2]=='shot')),
           'Attempt: {}'.format(a[column2].count()))


#gives yu the free throw numbers for a certain player
#for me column1 = 'player', column2='event_type', column3= 'result' name = player you wanna see
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

    s = ((' ', 'Shooting Percentage', 'Shots Made', 'Shots Attempted', 'FT Percentage', 'FT Made','FT Attempts'),(name1, (round(percenta1, 3)),(np.sum(a1[column2]=='shot')),
            (a1[column2].count()), (round(percenta2, 3)),(np.sum(a2[column3]=='made')),
           (a2[column3].count())),
            (name2, (round(percentb1, 3)),(np.sum(b1[column2]=='shot')),
            (b1[column2].count()), (round(percentb2, 3)),(np.sum(b2[column3]=='made')),
           (b2[column3].count())))
    
    g = pd.DataFrame(list(s)).T
    g.columns = g.iloc[0]
    g.drop(0, inplace=True)
    g = g.set_index(' ')
    return g

    


#groupby all the close games by player name and then give you how many games each player played
#col1: player and col2:game_id
def get_total_games(df, col1, col2):
    new_df = (df.groupby([col1, col2]).count()).reset_index()
    new_df = (new_df.groupby(col1).count()).reset_index()
    new_df = new_df[[col1,col2]]
    new_df = new_df.rename(columns={'game_id':'clutch_games'})
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


'''
#work on this 
def complete_comparison(df, column1, column2, column3, name1, name2):

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


    s = ((name1, "Shooting Percentage:{}".format(round(percenta1, 3)),'Made: {}'.format(np.sum(a1[column2]=='shot')),
            'Attempt: {}'.format(a1[column2].count()), "Free Throw:{}".format(round(percenta2, 3)),'Made: {}'.format(np.sum(a2[column3]=='made')),
           'Attempt: {}'.format(a2[column3].count())),
            (name2, "Shooting Percentage:{}".format(round(percentb1, 3)),'Made: {}'.format(np.sum(b1[column2]=='shot')),
            'Attempt: {}'.format(b1[column2].count()), "Free Throw:{}".format(round(percentb2, 3)),'Made: {}'.format(np.sum(b2[column3]=='made')),
           'Attempt: {}'.format(b2[column3].count())))
    
    g = pd.DataFrame(list(s)).T
    g.columns = g.iloc[0]
    g.drop(0, inplace=True)
    return g


'''












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
