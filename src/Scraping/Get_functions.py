from src.Utils import utils
from src.config import config

import requests
import pandas as pd
from bs4 import BeautifulSoup


class dic_players:
    def __init__(self):
        self.dic_players = {}

    def get_general_info(self, soup):
        '''

        Args:
            soup: soup where the information related to the general info is

        Returns:
            lista_f: list with the general information of the player
        '''
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

    def get_personal_data(self, soup):
        '''

        Args:
            soup: soup where the information related to the personal data is

        Returns:
            l_final: list with the personal data of the player
        '''
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

    def get_attributes_data(self, soup):
        '''

        Args:
            soup: where the information related to the attributes is

        Returns:
            lista_f: list with the attributes of the player
        '''
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

    def get_contractinfo_data(self, soup):
        '''

        Args:
            soup: soup where the information related to the contract is

        Returns:
            l_final: list with the contract information of the player

        '''
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

    def __join_lists(self, name_liga, player, l1, l2, l3, l4):
        '''

        Args:
            dic_players: dictionary with the information of the players
            name_liga: name of the league from the player
            player: name of the player
            l1: list with the general information of the player
            l2: list with the personal data of the player
            l3: list with the attributes of the player
            l4: list with the contract info of the player

        Returns:

        '''

        self.dic_players[player] = []
        self.dic_players[player].append(('Liga', name_liga))
        if l1 is not None:
            for elem in l1:
                try:
                    self.dic_players[player].append((elem[0], elem[1]))
                except:
                    pass
        if l2 is not None:
            for elem in l2:
                try:
                    self.dic_players[player].append((elem[0], elem[1]))
                except:
                    pass
        if l3 is not None:
            for elem in l3:
                try:
                    self.dic_players[player].append((elem[0], elem[1]))
                except:
                    pass
                self.dic_players[player].append((elem[0], elem[1]))
        if l4 is not None:
            for elem in l4:
                try:
                    self.dic_players[player].append((elem[0], elem[1]))
                except:
                    pass

    def get_urlteams(self, liga, name_liga):
        '''
        Get the url of the players of each team
        Args:
            liga: link of the league
            name_liga: name of the league

        Returns:
            own dictionary with the url of the players of each team
        '''

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
                self.get_info_player(url_player, name_liga)

        return self.dic_players

    def get_info_player(self, url_player, name_liga):
        '''

        Args:
            url_player: url of the player
            name_liga: name of the league from the player

        Returns:
            own dictionary with the all information of the player
        '''
        result = requests.get(url_player)
        src = result.content
        soup = BeautifulSoup(src, 'lxml')
        name_player = soup.find_all('h2', class_="title ta-c")
        print(name_player[0].text)
        # general_info
        l_general_info = self.__get_general_info(soup)
        l_personal_data = self.__get_personal_data(soup)
        l_atributos = self.__get_attributes_data(soup)
        l_contractinfo = self.__get_contractinfo_data(soup)

        self.dic_players = self.__join_lists(name_liga, name_player[0].text, l_general_info, l_personal_data, l_atributos,
                                 l_contractinfo)

    def get_final_df(self):
        col = set()
        for v in self.dic_players.values():
            for i in v:
                col.add(i[0])

        # transform col into a list
        col = list(col)

        # create a dataframe with the columns
        df = pd.DataFrame(columns=col)

        # iterate dic and fill the dataframe
        for k, v in self.dic_players.items():
            for i in v:
                df.loc[k, i[0]] = i[1]

        df.to_csv('info_players_v1.csv')
        return df





