import numpy as np
import pandas as pd
import requests
import json


def call_predict_function(x, y):
    # URL de tu función desplegada
    url = 'https://us-central1-upml2-420500.cloudfunctions.net/predict_function'

    # Datos que quieres enviar, ajusta según el formato esperado por tu función
    data = {
        "x": x,
        "y": y
    }

    # Convertir los datos a formato JSON
    json_data = json.dumps(data)

    # Enviar la solicitud POST a la función
    response = requests.post(url, data=json_data, headers={'Content-Type': 'application/json'})

    # Imprimir la respuesta recibida
    print("Status Code:", response.status_code)
    print("Response Body:", response.json())
    return response


def get_emojis():
	conceptos_con_emojis = {
      "Captación": "💰",
      "Seguro de Vida": "👨‍👩‍👧‍👦🛡️",  # Representa una familia y un escudo
      "Portabilidad": "📲",
      "Seguro de Salud": "🏥🛡️",
      "Crédito de Nómina": "💳🧾",
      "Seguro de Auto": "🚗🛡️",
      "Seguro de Hogar": "🏡🛡️",
      "Fondos": "💰💼",
      "Pagarés": "📝",
      "Tarjeta de Crédito": "💳",
      "Crédito Hipotecario": "🏠🏦",
      "PPI": "💸",
      "Crédito de Auto": "🚗💳",
      "EFI": "💵",
      "ILC": "📈💳"
    }
	return conceptos_con_emojis

def assigne_emoj(string, emoj):
	string = string.replace('Credito','Crédito').replace('Pagares','Pagarés').replace('Captacion','Captación').replace('Nomina','Nómina')
	for con, em in emoj.items():
		mostrar = em + con
		string = string.replace(con,mostrar)
	return string


def modelo(lista_top):
	return "Rock Clásico"


def get_genders():
	return ['acoustic',
 'punk-rock',
 'progressive-house',
 'power-pop',
 'pop',
 'pop-film',
 'piano',
 'party',
 'pagode',
 'opera',
 'new-age',
 'mpb',
 'minimal-techno',
 'metalcore',
 'metal',
 'mandopop',
 'malay',
 'latino',
 'latin',
 'kids',
 'k-pop',
 'jazz',
 'j-rock',
 'j-pop',
 'j-idol',
 'j-dance',
 'iranian',
 'psych-rock',
 'punk',
 'afrobeat',
 'r-n-b',
 'turkish',
 'trip-hop',
 'trance',
 'techno',
 'tango',
 'synth-pop',
 'swedish',
 'study',
 'spanish',
 'soul',
 'songwriter',
 'sleep',
 'ska',
 'singer-songwriter',
 'show-tunes',
 'sertanejo',
 'samba',
 'salsa',
 'sad',
 'romance',
 'rockabilly',
 'rock',
 'rock-n-roll',
 'reggaeton',
 'reggae',
 'industrial',
 'indie',
 'indie-pop',
 'indian',
 'disney',
 'disco',
 'detroit-techno',
 'deep-house',
 'death-metal',
 'dancehall',
 'dance',
 'country',
 'comedy',
 'club',
 'classical',
 'chill',
 'children',
 'chicago-house',
 'cantopop',
 'british',
 'breakbeat',
 'brazil',
 'blues',
 'bluegrass',
 'black-metal',
 'anime',
 'ambient',
 'alternative',
 'alt-rock',
 'drum-and-bass',
 'dub',
 'dubstep',
 'groove',
 'idm',
 'house',
 'honky-tonk',
 'hip-hop',
 'heavy-metal',
 'hardstyle',
 'hardcore',
 'hard-rock',
 'happy',
 'guitar',
 'grunge',
 'grindcore',
 'edm',
 'goth',
 'gospel',
 'german',
 'garage',
 'funk',
 'french',
 'forro',
 'folk',
 'emo',
 'electronic',
 'electro',
 'world-music']


def centroide_ponderado(generos, pesos, data_centroides):
    '''
    :param generos: lista con los tres generos escogidos por el usuario
    :param pesos: pesos asignados a los generos escogidos
    :param data_centroides: dataframe con los centroides de los géneros en el espacio 2D
    :return: coordenadas x,y del centroide de los generos escogidos
    '''
    dd = data_centroides[data_centroides.track_genre.isin(generos)]
    ddx = np.round((dd.x*pesos/sum(pesos)).sum(),8)
    ddy = np.round((dd.y*pesos/sum(pesos)).sum(), 8)
    return ddx, ddy
