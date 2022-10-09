import pyttsx3
import speech_recognition
import speech_recognition as sr
import pywhatkit
import yfinance as yf
import pyjokes
import webbrowser
import datetime
import wikipedia

#escuchar nuestro microfono y devolver el audio en texto
def transformar_audio_texto():

    #almacenar el reconigzer en variable
    r = speech_recognition.Recognizer()

    #configurar el microfono
    with sr.Microphone() as origen:

        #tiempo de espera
        r.pause_threshold = 0.8

        # informar que comenzó la grabación
        print("Ya puedes hablar")

        #Guardar lo que escuche como audio
        audio = r.listen(origen)

        try:
            #Buscar en google
            pedido = r.recognize_google(audio, language="es-py")

            # prueba de que pudo ingresar
            print("Dijiste " + pedido)

            #devolver a pedido
            return pedido
        #En caso de que no entienda
        except sr.UnknownValueError:

            #Prueba de que no entendio
            print("Ups no entendi")

            #devolver error
            return "Sigo esperando"

        except sr.RequestError:
            # Prueba de que no entendio
            print("Ups no hay servicio")

            # devolver error
            return "Sigo esperando"

        #error inesperado
        except:
            # Prueba de que no entendio
            print("Ups algo ha salido mal")

            # devolver error
            return "Sigo esperando"

# Funcon para que el asistente pueda ser escuchado
def hablar(mensaje):

    # encender el motor pyttsx3
    engine = pyttsx3.init()

    #pronunciar mensaje
    engine.say(mensaje)
    engine.runAndWait()


#informar el dia de la semana
def pedir_dia ():
    #crear la variable con datos de hoy
    dia = datetime.date.today()
    print(dia)

    #crear variable para día de la semana
    dia_semana = dia.weekday()
    print(dia_semana)

    #diccionario de los nombre de los días
    calendario = {0: 'Lunes',
                  1: 'Martes',
                  2: 'Miércoles',
                  3: 'Jueves',
                  4: 'Viernes',
                  5: 'Sábado',
                  6: 'Domingo'
                }

    # decir el día de la semana
    hablar(f'Hoy es {calendario[dia_semana]} {datetime.date.today()}')

#informar la hora
def pedir_hora():

    # crear una variable con datos de la hora
    hora = datetime.datetime.now()
    hora = f'En este momento son las {hora.hour} horas con {hora.minute} minutos y {hora.second} segundos'
    print(hora)

    # decir la hora
    hablar(hora)


# saludo inicial
def saludo_inicial():
    # Crear variable con datos de hora
    hora = datetime.datetime.now()
    if hora.hour < 6 or hora.hour > 20:
        momento = 'Buenas noches'
    elif 6 <= hora.hour < 13:
        momento = 'Buen día'
    else:
        momento = 'Buenas tardes'

    #Saludar
    hablar(f'{momento}, me presento, mi nombre es Ruth y estoy para ayudarle')

# Funcion central del asistente
def pedir_cosas():

    #activar el saludo inicial
    saludo_inicial()

    #Variable de corte
    comenzar = True

    while comenzar:
        #activar el micro y guardar el pedido en un string
        pedido = transformar_audio_texto().lower()

        if 'abrir youtube' in pedido:
            hablar('Con gusto, abriendo YouTube')
            webbrowser.open('https://youtube.com/')
            continue
        elif 'abrir navegador' in pedido:
            hablar('Claro, estoy en eso')
            webbrowser.open('https://google.com')
            continue
        elif 'Que día es hoy' in pedido:
            pedir_dia()
            continue
        elif 'Que hora es' in pedido:
            pedir_hora()
            continue
        elif 'Buscar en wikipedia' in pedido:
            hablar('Buscando eso en wikipedia')
            pedido = pedido.replace('buscar en wikipedia', '')
            wikipedia.set_lang('es')
            resultado = wikipedia.summary(pedido, sentences=1)
            hablar('Wikipedia dice lo siguiente:')
            hablar(resultado)
            continue
        elif 'Buscar en internet' in pedido:
            hablar('Buscando eso en google')
            pedido.replace('buscar en internet', '')
            pywhatkit.search(pedido)
            hablar('Esto es lo que he encontrado')
            continue
        elif 'reproducir' in pedido:
            hablar('Que buena eleccion musical, ya mismo lo reproduzco')
            pywhatkit.playonyt(pedido)
            continue
        elif 'chiste' in pedido:
            hablar(pyjokes.get_joke('es'))
            continue
        elif 'precio de las acciones' in pedido:
            accion = pedido.split('de')[-1].strip()
            cartera = {'apple': 'APPL',
                       'amazon': 'AMZN',
                       'google': 'GOOGL'}
            try:
                accion_buscada = cartera[accion]
                accion_buscada = yf.Ticker(accion_buscada)
                precio_actual = accion_buscada.info['regularMarketPrice']
                hablar(f'La encontré, el precio de {accion} es de {precio_actual} por acción')
                continue
            except:
                hablar('Perdón no la he encontrado')
                continue
        elif 'chao' in pedido:
            hablar('Me voy a descansar, cualquier cosa me avisas')
            break


pedir_cosas()