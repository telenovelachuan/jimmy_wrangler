import pandas as pd
from difflib import SequenceMatcher


raw_EPL_tables = pd.read_csv("../data/raw/english-football-premier-league-tables-1968-2019.csv")
raw_match_stat = pd.read_csv("../data/interim/2013_2019_with_date_transformed.csv")

'''
Raw match stats dataset:
       Date  HomeTeam       AwayTeam  FTHG  FTAG  ...   HY   AY   HR   AR Season
0  19/08/00  Charlton       Man City   4.0   0.0  ...  1.0  2.0  0.0  0.0  00-01
1  19/08/00   Chelsea       West Ham   4.0   2.0  ...  1.0  2.0  0.0  0.0  00-01
2  19/08/00  Coventry  Middlesbrough   1.0   3.0  ...  5.0  3.0  1.0  0.0  00-01
3  19/08/00     Derby    Southampton   2.0   2.0  ...  1.0  1.0  0.0  0.0  00-01
4  19/08/00     Leeds        Everton   2.0   0.0  ...  1.0  3.0  0.0  0.0  00-01

Raw EPL tables dataset:
      season                      name  pos  ...   a  gd  points
0  2018/2019  Premier League 2018-2019    1  ...  23  72      98
1  2018/2019  Premier League 2018-2019    2  ...  22  67      97
2  2018/2019  Premier League 2018-2019    3  ...  39  24      72
3  2018/2019  Premier League 2018-2019    4  ...  39  28      71
4  2018/2019  Premier League 2018-2019    5  ...  51  22      70

'''

distinct_team_name_in_EPL_table = raw_EPL_tables['team'].unique()

# find the most similar team name in EPL tables dataset


def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()


for i, row in raw_match_stat.iterrows():
    home_team_name = row.HomeTeam
    away_team_name = row.AwayTeam
    if (not isinstance(home_team_name, str)) or (not isinstance(away_team_name, str)):
        continue
    similarities_home = [similarity(home_team_name, team_name) for team_name in distinct_team_name_in_EPL_table]
    similarities_away = [similarity(away_team_name, team_name) for team_name in distinct_team_name_in_EPL_table]
    most_similar_home_name = distinct_team_name_in_EPL_table[similarities_home.index(max(similarities_home))]
    most_similar_away_name = distinct_team_name_in_EPL_table[similarities_away.index(max(similarities_away))]
    raw_match_stat.set_value(i, 'HomeTeam', most_similar_home_name)
    raw_match_stat.set_value(i, 'AwayTeam', most_similar_away_name)


print raw_match_stat.head()
raw_match_stat.to_csv(index=False, path_or_buf="../data/interim/2013_2019_with_date_transformed_full_team_name.csv")

