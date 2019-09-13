import pandas as pd

interim_match_data = pd.read_csv("../data/interim/2013_2019_with_date_transformed_full_team_name.csv")
interim_EPL_tables = pd.read_csv("../data/interim/EPL-tables-1968-2019_with_splitted_year.csv")

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

Join two datasets to append final finish position info for match stats
'''

home_positions = []
away_positions = []
for i, row in interim_match_data.iterrows():
    home_team_name = row.HomeTeam
    away_team_name = row.AwayTeam
    year1 = row.year if row.month > 7 else row.year - 1
    home_final_position = interim_EPL_tables[(interim_EPL_tables.team == home_team_name) & (interim_EPL_tables.year1 == year1)].pos.item()
    away_final_position = interim_EPL_tables[(interim_EPL_tables.team == away_team_name) & (interim_EPL_tables.year1 == year1)].pos.item()
    home_positions.append(home_final_position)
    away_positions.append(away_final_position)

interim_match_data['home_final_position'] = pd.Series(home_positions)
interim_match_data['away_final_position'] = pd.Series(away_positions)

print interim_match_data.head()
interim_match_data.to_csv(index=False, path_or_buf="../data/interim/2013_2019_new_date_full_team_name_pos.csv")


