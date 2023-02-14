from src.config import config
from src.Scraping.Get_functions import get_urlteams, get_final_df

for liga, equipo in zip(config.ligas, config.name_ligas):
    dic_players = get_urlteams(liga, equipo, dic_players)


df = get_final_df(dic_players)

