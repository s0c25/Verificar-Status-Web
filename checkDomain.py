import requests
from bs4 import BeautifulSoup
import sys

# Token de tu bot y ID CHAT para obtenerlo debes ver el getupdate de tu bot
# https://api.telegram.org/bot<AQUIVATUTOKEN>/getUpdates

TOKEN = ''
chat_id = '' 

# Método para enviar un mensaje
def send_message(chat_id, text):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {'chat_id': chat_id, 'text': text}
    response = requests.post(url, data=payload)
    return response.json()



# URL de la página a buscar
url = ["https://google.com.ve/"
       ,"https://xvideos.com/"
       ,"https://beeg.com/"
       ]
       
# Buscar un texto específico en la página
texto_buscado = ["This Account has been suspended."
            ,"Error establishing a database connection"
            ]
            
for index,elemento in enumerate(url):
    try:
            response = requests.get(elemento)
            html = response.content
            # Crear objeto BeautifulSoup para analizar el contenido HTML
            soup = BeautifulSoup(html, "html.parser")
            
           
            #arreglo de url con error
            web_error = []
            #arreglo de url con con exito
            web_ok = []
            
            if response.status_code == 200:
                for texto in texto_buscado:
                    if texto in soup.get_text():
                        text = f"El texto ({texto}) fue encontrado en la página {elemento}"
                        web_error.append(elemento)
                        # print (url)
                        send_message(chat_id, text)
                    #check si existen coincidencia para no repetir el envio de mensaje
                    elif set(url).intersection(set(web_error)):
                        print(f"Los arreglos tienen coincidencia para la url {elemento}")
                    #check si existen coincidencia para no repetir el envio de mensaje
                    elif set(url).intersection(set(web_ok)):
                        print(f"Los arreglos tienen coincidencia para la url {elemento} ya que las web estan OK!!")
                    else:
                        web_ok.append(elemento)
                        text = f"La pagina {elemento} se encuentra OK!!"
                        send_message(chat_id, text)

            elif response.status_code != 200:
                text = f"Esto significa que la web {elemento} no posee un status {response.status_code} revisar"
                send_message(chat_id, text)
            else:
                text = f"Esto significa que la web {elemento} posee un error en el arreglo. Debe estar mal escrito"
                send_message(chat_id, text)


    except requests.exceptions.ConnectionError as e:
        text = f"Error de conexión: {e.args[0]}"
        send_message(chat_id, text)
    except requests.exceptions.HTTPError as e:
        text = f"Error HTTP: {e.args[0]}"
        send_message(chat_id, text)
    except requests.exceptions.Timeout as e:
        text = f"Tiempo de espera agotado: {e.args[0]}"
        send_message(chat_id, text)
    except requests.exceptions.TooManyRedirects as e:
        text = f"Demasiados redireccionamientos: {e.args[0]}"
        send_message(chat_id, text)
    except requests.exceptions.RequestException as e:
        text = f"Error inesperado: {e.args[0]}"
        send_message(chat_id, text)





