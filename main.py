from src.config import config
from src.Scraping.Get_functions import dic_players
import pandas as pd
from src.Scraping.Cleaning_data import df_to_dic, clean_data

dic_players = dic_players()

for liga, equipo in zip(config.ligas, config.name_ligas):
    dic_players = dic_players.get_urlteams(liga, equipo, dic_players)

df = dic_players.get_final_df()

df = pd.read_csv('info_players_v1.csv')

dic = df_to_dic(df)

dic_clean = clean_data(dic)

df_clean = pd.DataFrame(dic)

df_clean.to_csv('info_players_clean_data.csv', sep=',')
