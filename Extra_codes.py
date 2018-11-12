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