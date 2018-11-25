# clutch-baller
who is the most clutch player?

-What is the project?
To see who was a clutch player in NBA in the past and who will be more clutch next season.

-Why do it?
To answer wether there is such thing as clutch.
Is the best player in the team the most clutch
Help determine who should take more shots in the closing momemts of the game when the game is close.

-How did you get the answer?
Looked at the play by play stats for each game in last 14 years.
Focus on games that were within 6 points with two minutes to play in the regulation.
Get stats for each player for these conditions.
Compare them with the rest of the league and with the non-clutch time.
Came up with a clutch score and if a players clutch score is above the league average and has taken a certain amount of shots then the player is considered clutch.

-Model results?
Looked at the stats from last year and predict if the player will be clutch next year.
there were 8 important features.
Did gradient boosting and the model predicted correctly with the accuracy of 87.3%. Which was higher than the baseline model which predicted correctly with the accuracy of only 68%. Baseline model was if the player is clutch last year, they will be clutch again next year.

-What were the findings?
All the players shooting percentages go doen by 5-6% in last two minutes. Only 12 players were clutch last year. Some big name players were not good in these clutch moments.


-Future Studies?
Look at other factors that can impact the clutchness.
Add defensive stats to see if they are clutch.
Look at defensive plays, was the player double teamed or one on one.
Was the shot contested or open shot.
