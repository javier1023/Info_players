from bs4 import BeautifulSoup
import requests
import pandas as pd

from src.config import config
from src.Utils import utils

dic_players = {}


def get_urlteams(liga, name_liga, dic_players):
    dic = {}
    result = requests.get(liga)
    src = result.content
    soup = BeautifulSoup(src, 'lxml')
    equipos = soup.find_all('td', class_='name')
    for equipo in equipos:
        equipo = equipo.find('span', class_="team-name").text
        squad = config.squads[0]
        squad_team = squad + f'{utils.normalize(equipo.lower().replace(" ", ""))}'
        result_team = requests.get(squad_team)
        src_team = result_team.content
        soup_team = BeautifulSoup(src_team, 'lxml')
        feat = soup_team.find_all('td', class_='name')
        for f in feat:
            url_player = f.find_all('a')
            url_player = url_player[0]['href']
            get_info_player(url_player, name_liga, dic_players)


    return dic_players


def get_info_player(url_player, name_liga, dic_players):
    result = requests.get(url_player)
    src = result.content
    soup = BeautifulSoup(src, 'lxml')
    name_player = soup.find_all('h2', class_="title ta-c")
    print(name_player[0].text)
    # general_info
    l_general_info = get_general_info(soup)
    l_personal_data = get_personal_data(soup)
    l_atributos = get_attributes_data(soup)
    l_contractinfo = get_contractinfo_data(soup)

    dic_players = join_lists(dic_players, name_liga, name_player[0].text, l_general_info, l_personal_data, l_atributos,
                             l_contractinfo)


def join_lists(dic_players, name_liga, player, l1, l2, l3, l4):
    dic_players[player] = []
    dic_players[player].append(('Liga', name_liga))
    if l1 is not None:
        for elem in l1:
            try:
                dic_players[player].append((elem[0], elem[1]))
            except:
                pass
    if l2 is not None:
        for elem in l2:
            try:
                dic_players[player].append((elem[0], elem[1]))
            except:
                pass
    if l3 is not None:
        for elem in l3:
            try:
                dic_players[player].append((elem[0], elem[1]))
            except:
                pass
            dic_players[player].append((elem[0], elem[1]))
    if l4 is not None:
        for elem in l4:
            try:
                dic_players[player].append((elem[0], elem[1]))
            except:
                pass


def get_general_info(soup):
    lista_f = []
    # First I will extract general info
    general_info_url = soup.find_all('div', class_="panel-body stat-list")
    for elem in general_info_url:
        general_info = elem.find_all('div', class_="big-row")
        for i, sp_info in enumerate(general_info):
            lista = []
            lista.append(sp_info.text)
            lista.append(config.caracteristicas[i])
            lista.reverse()
            lista_f.append(lista)
    return lista_f


def get_personal_data(soup):
    # More info
    l_final = []
    info = soup.find_all('div', class_="panel-body table-list")
    for type_info in info:
        # Personal data
        # print(type_info)
        description = type_info.find_all('div', class_="table-head")
        if description[0].text == 'Personal data':
            personal_data = type_info.find_all('div', class_="table-row")
            for pers_data in personal_data:
                l = pers_data.text.split('\n')
                l = utils.delete_empty_values(l)
                l_final.append(l)
            break
    return l_final


def get_attributes_data(soup):
    # Attributes
    l_final = []
    i = 0
    for i in range(1, 7):
        attributes = soup.find_all('div', class_=f"cl-name slice-{i}")
        for elem in attributes:
            lista = elem.text.split('\n')
            lista = utils.delete_empty_values(lista)
            lista.reverse()
            l_final.append(lista)
    return l_final


def get_contractinfo_data(soup):
    # CONTRACT INFORMATION
    l_final = []
    tables = soup.find_all('div', class_="table-body")
    try:
        for elem in tables[8]:
            lista = elem.text.split('\n')
            lista = utils.delete_empty_values(lista)
            if len(lista) > 0:
                l_final.append(lista)
        return l_final
    except:
        pass



def get_final_df(dic):
    col = set()
    for v in dic.values():
        for i in v:
            col.add(i[0])

    # transform col into a list
    col = list(col)

    # create a dataframe with the columns
    df = pd.DataFrame(columns=col)

    # iterate dic and fill the dataframe
    for k, v in dic.items():
        for i in v:
            df.loc[k, i[0]] = i[1]

    df.to_csv('info_players_v1.csv')
    return df

