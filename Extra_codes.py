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
                                 
