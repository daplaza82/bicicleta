import urllib.request
import json
import os
import ssl

def allowSelfSignedHttps(allowed):
    # Bypass the server certificate verification on the client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

allowSelfSignedHttps(True)  # This line is needed if you use a self-signed certificate in your scoring service.

# Solicitar al usuario que ingrese los valores para los campos de "data"
day = int(input("Ingrese el día: "))
month = int(input("Ingrese el mes: "))
year = int(input("Ingrese el año: "))
season = int(input("Ingrese la estación (1 para primavera, 2 para verano, 3 para otoño, 4 para invierno): "))
holiday = int(input("¿Es día festivo? (1 para sí, 0 para no): "))
weekday = int(input("Ingrese el día de la semana (1 para lunes, 2 para martes, ..., 7 para domingo): "))
workingday = int(input("¿Es día laborable? (1 para sí, 0 para no): "))
weathersit = int(input("Ingrese la situación climática (1 para despejado, 2 para nublado, 3 para lluvioso): "))
temp = float(input("Ingrese la temperatura (en grados Celsius): "))
atemp = float(input("Ingrese la sensación térmica (en grados Celsius): "))
hum = float(input("Ingrese la humedad relativa (0.0 a 1.0): "))
windspeed = float(input("Ingrese la velocidad del viento (en km/h): "))

# Crear el diccionario con los valores ingresados por el usuario
user_data = {
    "day": day,
    "mnth": month,
    "year": year,
    "season": season,
    "holiday": holiday,
    "weekday": weekday,
    "workingday": workingday,
    "weathersit": weathersit,
    "temp": temp,
    "atemp": atemp,
    "hum": hum,
    "windspeed": windspeed
}

# Crear el objeto JSON con los datos del usuario
data = {"Inputs": {"data": [user_data]}, "GlobalParameters": 1.0}

body = str.encode(json.dumps(data))

url = 'http://2f1592b3-57aa-4905-8783-5dfa709b497f.centralus.azurecontainer.io/score'
# Reemplazar esto con la clave primaria/secundaria, AMLToken o el token de Microsoft Entra para el punto final
api_key = 'D7rJmF2GTCwnWmC39JJGDnxAyig5vDPd'
if not api_key:
    raise Exception("Se debe proporcionar una clave para invocar el punto final")

headers = {'Content-Type': 'application/json', 'Authorization': ('Bearer ' + api_key)}

req = urllib.request.Request(url, body, headers)

try:
    response = urllib.request.urlopen(req)
    result = response.read()
    print(result)
except urllib.error.HTTPError as error:
    print("La solicitud falló con el código de estado: " + str(error.code))
    # Imprimir los encabezados: incluyen el ID de la solicitud y la marca de tiempo, útiles para depurar el fallo
    print(error.info())
    print(error.read().decode("utf8", 'ignore'))