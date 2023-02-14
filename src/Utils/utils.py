from src.config import config

def normalize(s):
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
    )
    for a, b in replacements:
        s = s.replace(a, b).replace(a.upper(), b.upper())
    return s


def delete_empty_values(lista):
    l2 = []
    for elem in lista:
        if elem != '':
            l2.append(elem.replace(' ', ''))
    return l2

def date_of_birth(text):
    long_text = len(text)
    long_month = long_text - 6.  # Day and year always have 2 and 4 carácteres respectively. So for the month we have to substract 6
    if text == 'nan':
        return text
    else:
        return text[0:2] + '-' + config.date_of_birth[text[2:int(long_month+2)]] + '-' + text[int(long_month+2):int(long_text)]
