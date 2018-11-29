#codes that i didnt use but maybe usefull

x = regular_season.loc[(regular_season['type']=='rebound offensive'), 'player']

#all the offensive rebounds are grouped by player names and shows how many offensive 
#rebounds they had in each game
a = (rebound_type.groupby(['player', 'game_id']).count()).reset_index()

#takes all the players from a and add all all the games they apperaed in
b = (a.groupby('player').count()).reset_index()
b = b[['player', 'game_id']]




#merge b with rebound_per_player to show how many games a player played in
#and how many total rebounds they got
d = b.merge(rebound_per_player,on='player')

k = d.drop('game_id', axis = 1)




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
        
        
        
df.dropna(subset=['assist'], inplace=True)    




##Use this when combining codes for assist, blocks, rebousds:

    intangible_feature = off_reb_df(df,col1)
    
    intangible_dic= {}
    for value in intangible_feature['assist'].values:
        if value not in blk_dic.keys():
            intangible_dic[value]=1
        else:
            blk_dic[value]+=1


    new_df = pd.DataFrame.from_dict(intangible_dic,orient = 'index')
    new_df = new_df.reset_index()
    
    if col1 == 'block':
        new_df = new_df.rename(columns={'index':'player', 0:'total_blocks'})
    
    if col1 == 'assist':
        new_df = new_df.rename(columns={'index':'player', 0:'total_assist'})

    total_games = get_total_games(df, col2, col3)

    l = total_games.merge(new_df, on = col2)
    
    
    
    
    
    
    
    

#Try t get everything in one code    
    
    
def clutch_per_game(df, col1, col2, col3):

    intangible_feature = get_intangibles(df,col1)

    rebound_dic = {}
    assist_dic = {}
    blk_dic = {}

    for value in intangible_feature[col1].values:
        if col1 == 'off_rebound':
            if value not in blk_dic.keys():
                blk_dic[value]=1
            else:
                blk_dic[value]+=1

        if col1 == 'assist':
            if value not in assist_dic.keys():
                assist_dic[value]=1
            else:
                assist_dic[value]+=1

        if col1 == 'block':
            if value not in rebound_dic.keys():
                rebound_dic[value]=1
            else:
                rebound_dic[value]+=1


        if col1 == 'off_rebound':            
            rebound_per_player = pd.DataFrame.from_dict(intangible_dic,orient = 'index')
            rebound_per_player = rebound_per_player.reset_index()
            rebound_per_player = rebound_per_player.rename(columns={'index':'player', 0:'total_rebound'})

            total_games = get_total_games(df, col2,col3)

        #merge two df so we get total games played and total offensive rebounds for each player
            off_rebounds = total_games.merge(rebound_per_player, on = 'player')

        #create a new column with off_rebund per game
            off_rebounds['off_rebound/clutch time']=off_rebounds.apply(lambda row: row.total_rebound / row.clutch_games, axis = 1)

            l = off_rebounds.sort_values(by = ['total_rebound', 'clutch_games'], ascending=False)



        if col1 == 'assist':
            assist_per_player = pd.DataFrame.from_dict(assist_dic,orient = 'index')
            assist_per_player = assist_per_player.reset_index()
            assist_per_player = assist_per_player.rename(columns={'index':'player', 0:'total_assist'})

            total_games = get_total_games(df, col2, col3)

            c = total_games.merge(assist_per_player, on = col2)

            #create a new column with assists per game

            c['assist_per_clutch_time']=c.apply(lambda row: row.total_assist / row.clutch_games, axis =1)

            #sorted by amount of games and assists

            l = c.sort_values(by = ['total_assist', 'clutch_games'], ascending=False)





        if col1 == 'block':
            blocks_1 = pd.DataFrame.from_dict(blk_dic,orient = 'index')
            blocks_1 = blocks_1.reset_index()
            blocks_1 = blocks_1.rename(columns={'index':'player', 0:'total_blocks'})

            total_games = get_total_games(df, col2, col3)

            d = total_games.merge(blocks_1, on = col2)

            #create a new column with assists per game

            d['block_per_clutch_time']=d.apply(lambda row: row.total_blocks / row.clutch_games, axis =1)

            #sorted by amount of games and assists

            l = d.sort_values(by = ['total_blocks', 'clutch_games'], ascending=False)

        return l    
    
    
    
    
    
    
    
    fig, axs = plt.subplots(1,0, figsize=(12,8))
plt.hist(x['pts_difference'], bins= 50);




'''Took from individaul.py was used to add extra columns which was later done in practice code'''


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







#if reg season was clutch

full_reg_stats['reg_all_shots'] = (full_reg_stats['shooting%'] > full_reg_stats['league_reg_all_shot_avg']) & (full_reg_stats['total_shots']>15)
full_reg_stats['reg_2pt'] = (full_reg_stats['2pt%'] > full_reg_stats['league_reg_2pt_avg']) & (full_reg_stats['total_shots']>15)
full_reg_stats['reg_3pt'] = (full_reg_stats['3pt%'] > full_reg_stats['league_reg_3pt_avg']) & (full_reg_stats['total_shots']>15)
full_reg_stats['reg_hard2'] = (full_reg_stats['med/hard_fg%'] > full_reg_stats['league_reg_hard2pt_avg']) & (full_reg_stats['total_shots']>15)
full_reg_stats['reg_easy2'] = (full_reg_stats['easy_shot%'] > full_reg_stats['league_reg_easy2pt_avg']) & (full_reg_stats['total_shots']>15)






#Old code for ic_clucth

def is_clutch(df):
    df = df[df['total_games']>41]
    df['clutch_all_shots'] = (df['shooting%'] > df['league_all_shot_avg']) & (df['total_shots']>30)
    df['clutch_2pt'] = (df['2pt%'] > df['league_2pt_avg']) & (df['2fg_attempts']>25)
    df['clutch_3pt'] = (df['3pt%'] > df['league_3pt_avg']) & (df['3pt_shots']>15)
    df['clutch_hard2'] = (df['med/hard_fg%'] > df['league_hard2pt_avg']) & (df['med/hard_attempts']>10)
    df['clutch_easy2'] = (df['easy_shot%'] > df['league_easy2pt_avg']) & (df['Dunk/Layup_attempts']>10)
    
    df['clutch FT'] = df['FT%'] > df['league_ft%']
    df['clutch_oreb'] = df['ORPG'] > df['league_oreb_avg']
    df['clutch_blks'] = df['BPG'] > df['league_blks_avg']
    df['clutch_asts'] = df['APG'] > df['league_ast_avg']
#    df['clutch_TO'] = df['TPG'] < df['league_TO_avg']
#    df['clutch_ejections'] = df['ejections'] < df['ejections/career']





#gives yu the free throw numbers for a certain player
#for me column1 = 'player', column2='event_type', column3= 'result' name = player you wanna see
def free_throw_percent(df,name):
    b = df[(df['player']==name) & (df['event_type'] == 'free throw') & ((df['result']== 'made')|
                                        (df['result']=='missed'))]
    percent = np.sum(b['result']=='made')/b['result'].count()
    return("Free Throw:{}".format(round(percent, 3)),'Made: {}'.format(np.sum(b['result']=='made')),
           'Attempt: {}'.format(a['result'].count()))

    


                                 
#gives you the shooting percent
#for me column1 = 'player', column2='event_type', name = player you wanna see
def get_percent(df, name):
    a = df[(df['player']==name) & ((df['event_type']== 'miss')|(df['event_type']=='shot'))]
    b = df[(df['player']==name) & (df['event_type'] == 'free throw') & ((df['result']== 'made')|
                                        (df['result']=='missed'))]
    
    percent_a = np.sum(a['event_type']=='shot')/a['event_type'].count()
    
    percent_b = np.sum(b['result']=='made')/b['result'].count()

    result = ((' ', 'Shooting Percentage', 'Shots Made', 'Shots Attempted', 'FT Percentage', 'FT Made','FT Attempts'), 
              (name, (round(percent_a, 3)),(np.sum(a['event_type']=='shot')), (a['event_type'].count()), (round(percent_b, 3)),
               (np.sum(b['result']=='made')), (b['result'].count())))
                     

    df = pd.DataFrame(list(result)).T
    df.columns = df.iloc[0]
    df.drop(0, inplace=True)
    df = df.set_index(' ')
    return df




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



#Get complete stats for a player
def player_stat(name1, name2):
    player1 = (clutch_stats.loc[clutch_stats['player'] == name1]) 
    player2 = (clutch_stats.loc[clutch_stats['player'] == name2])
    both = pd.merge(player1,player2, how = 'outer')
    both = both.T
    both.reset_index(level=0, inplace=True)
    both.columns = both.iloc[0]
    stats = both.reindex(both.index.drop(0))
    stats = stats.rename(columns={'player':' '})
    stats = stats.set_index(' ')
    stats = stats.drop(['shots_made', '2pt_made', '3pt_made', 'FT_made'])
    return stats




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