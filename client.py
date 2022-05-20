import requests
import time
import os

url = 'http://192.168.56.1:8080' 

# response = requests.get(url+'/ding.jpg')
# metodo = input("¿Qué método desea usar? escriba: get | post | head ").casefold()

# match metodo:
#     case "post": 
# archivo = input("Indique la ruta del archivo local: ")
archivo = 'files\\logo.png'
nombreDeArchivo = archivo[archivo.rindex('\\')+1:]

try:
    f = open(archivo, 'rb')
    response_data = f.read()
    f.close()
except Exception as e:
    print('file not found', e)

response = requests.post(url, data={"content": nombreDeArchivo, "archivo": response_data})

    # case "get":
    #     nombreDelArchivo = input("Indique el nombre del archivo: ")

    #     response = requests.get(url+ "/" + nombreDelArchivo)
    # case "head":
    #     nombreDelArchivo = input("Indique la ruta del archivo: ")

    #     response = requests.head(url+ "/" + nombreDelArchivo)

# response = requests.post(url, data={"test1": "value1", "test2": "value2"})

print(response.status_code)
# time.sleep(10)

# response = requests.post(url, data={"content": nombreDeArchivo, "archivo": response_data})
# print(response.status_code)