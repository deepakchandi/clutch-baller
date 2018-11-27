# clutch-baller
who will be clutch in next season?

Every sports enthusiast have had some type of argument about the sport they love. In NBA one of the most hot topics is "who is the most clutch player?" In this project, I looked at the NBA play by play data fro each game from last 14 season to see who has been a clutch player in NBA in the past and predict who will be more clutch next season. The goal was to see which players should take more shots in closing moments of a close game. I defined the clutch moment being a game that is within 6 points with only two minutes to play in the fourth quarter.

First step was to do some EDA, feature engineering, and then get only the games that were clutch, within 6 points with two minutes to play. Then, I got stats for every player that played with in the clutch time. The next step was to see if there is any difference between regular game and the clutch time. For that I followed the same procedure for the games that were not clutch and for all the games before 2 minutes of regulation. After comparing the player stats for both I found out that all the players are less efficient in last two minutes, in comparison to rest of the game.

After looking some more data engineering I came up with a clutch score for each player depending on how well they performed during that time. Then, by looking at the clutch score and other stats I labled each player as clutch or not clutch. Out of all the players about 16% ended up being clutch.


Next step was to predict who will be clutch next year by looking at the stats from previous year. For this I tried Random Forest, gradient boosting, and the XGBoost. I decided to go with the XGBoost as it gave slightly better results. After running the final test, my model gave F1 score of 33% which was 14% improvement from the baseline model


-Future Studies?
Look at other factors that can impact the clutchness.
Add defensive stats to see if they are clutch.
Look at defensive plays, was the player double teamed or one on one.
Was the shot contested or open shot.
