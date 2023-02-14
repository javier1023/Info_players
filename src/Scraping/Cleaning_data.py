
import pandas as pd
from src.Utils import utils



def df_to_dic(df):
    dic = {}
    for col in df.columns:
        if col == 'Unnamed: 0':
            dic['Name'] = []
            for row in df[col]:
                dic['Name'].append(row)
        else:
            dic[col] = []
            for row in df[col]:
                dic[col].append(row)
    return dic

def clean_data(dic):
    for col, values in dic.items():
        if col == 'Salary':
            for i in range(len(values)):
                if type(values[i]) == str:
                    current = values[i][:-7]
                    if current[-1] == 'M':
                        values[i] = float(current[:-1]) * 1000
                    else:
                        values[i] = current[:-1]

        elif col == 'Ageondebut':
            for i in range(len(values)):
                if type(values[i]) == str:
                    values[i] = values[i][:-6]
        elif col == 'Dateofbirth':
            for i in range(len(values)):
                if type(values[i]) == str:
                    values[i] = utils.date_of_birth(values[i])
        elif col == 'Marketvalue':
            for i in range(len(values)):
                if type(values[i]) == str:
                    values[i] = values[i][:-2]
        elif col == 'Totaltransfer':
            for i in range(len(values)):
                if type(values[i]) == str:
                    values[i] = values[i][:-2]
        elif col == 'CIESvalue':
            for i in range(len(values)):
                if type(values[i]) == str:
                    values[i] = values[i][:-2]
        elif col == 'TMvalue':
            for i in range(len(values)):
                if type(values[i]) == str:
                    values[i] = values[i][:-2]
        elif col == 'Releaseclause':
            for i in range(len(values)):
                if type(values[i]) == str:
                    values[i] = values[i][:-2]
    return dic

# creating a new dataframe with the cleaned data
df_clean = pd.DataFrame(dic)

df_clean.to_csv('info_players_clean_data.csv', sep=',')
