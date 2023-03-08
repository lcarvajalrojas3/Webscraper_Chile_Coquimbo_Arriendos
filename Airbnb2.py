from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options ### CONFIGURADO CON EDGE
import pandas as pd
from datetime import datetime, timedelta
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
#import cv2
#import pytesseract
import base64
import numpy as np
import os
import random
import string

"""
FUNCIONES DESARROLLADAS
TEMA - FUNCIÓN

GENERACIÓN DE CARPETAS
    f(x) def create_folders() >>> Genera una carpeta donde guardar los df por iteración (búsqueda).

APERTURA INICIAL
    f(x) def opendriver(options) >>> Abre y define el driver para su ejecución
    f(x) def apertura_marketplace(driver, busqueda) >>> Abre la primera página de resultados de una búsqueda. Se debe proveer la url de esta página inicial,
                                                        no realiza la búsqueda en sí.
    f(x) def aplicar_filtros(driver, nfiltro) >>> Aplica filtros para reducir el tamaño de la muestra que entrega Airbnb. Se reduce a "nfiltro" Contiene subfunciones
        f(x) def filter_noptions(lista1, lista2) ¬¬¬ Reduce las opciones de selección de primer criterio
        f(x) def tipo_filtro(divs) ¬¬¬ Selecciona segundo criterio
        f(x) def servicio_filtro(divs) ¬¬¬ Aplica 3er criterio sumando opciones hasta reducir el tamaño de la muestra a lo deseado

CARGA DE LINKS Y SCRAP DE INFO
    f(x) def scrap_items(driver, df) >>> Desde la página de lista de avisos, compila los links, abre cada uno y aplica la subfunción scrap, para luego invocar función de nextpage.
                                         Contiene la capacidad de terminar el scrapping por que no hayan más links para scrapping, o por bug.
        f(x) def scrap(driver, link, df) ¬¬¬ Desde el anuncio abierto, extrae la info requerida en df central
        f(x) def siguiente_pagina(driver, df) ¬¬¬ Desde la página de resultados de búsqueda, carga la siguiente página. En caso de no haber siguiente página, termina

PROCESADO DE DF
    f(x) def pre_procesado(df) >>> Adapta y trata datos de Df para su posterior exportación.

"""

options = Options()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument("--disable-notifications")

def create_folders():
    print("\n\nRevisando existencia de carpetas necesarias")
    dir_path = os.path.dirname(os.path.realpath(__file__))
    print("path local: ", dir_path)
    folderpath = "Airbnb"
    folderpath = os.path.join(dir_path, folderpath)
    if not os.path.exists(folderpath):
        os.mkdir(folderpath)
        print("Carpeta Airbnb creada")
    else: print("Carpeta Airbnb existente")
    dir_path = folderpath
    folderpath = "Prueba2"
    folderpath = os.path.join(dir_path, folderpath)
    if not os.path.exists(folderpath):
        os.mkdir(folderpath)
        print("Subcarpeta Data creada\n\n")
    else: print("Subcarpeta Data Existente")
    return folderpath

def opendriver(options):
    driver = webdriver.Chrome(options=options)
    time.sleep(2)
    driver.maximize_window()
    print("Abriendo WebDriver")
    time.sleep(2)
    return driver

def apertura_marketplace(driver, busqueda):
    airbnburl = "https://www.airbnb.cl/"
    driver.get(airbnburl)
    time.sleep(3)
    print("Cargando Airbnb y realizando búsqueda de '", busqueda, "'")
    buscador = driver.find_element(By.XPATH,'//div[contains(text(), "En cualquier lugar del mundo")]/..')
    buscador.click()
    time.sleep(1)
    buscador = driver.find_element(By.XPATH, '//input[@id="bigsearch-query-location-input"]')
    #buscador.clear()
    #buscador.send_keys(Keys.CONTROL, "a")
    #buscador.send_keys(Keys.DELETE)
    buscador.send_keys(busqueda)
    button = driver.find_element(By.XPATH,'//button[@data-testid="structured-search-input-search-button"]')
    button.click()
    time.sleep(3)

def aplicar_filtros(driver, nfiltro):
    
    button = driver.find_element(By.XPATH, '//button[@style="--filter-button_border:1px solid var(--j-qkgmf);"]')
    button.click()
    time.sleep(1)
    
    divs = driver.find_element(By.XPATH, '(//*[@id="site-content"])[2]')
    
    options = divs.find_elements(By.XPATH, './div[3]//section/div[2]/div')
    rooms = options[0].find_elements(By.XPATH, ".//button")
    beds = options[1].find_elements(By.XPATH, ".//button")
    baths = options[2].find_elements(By.XPATH, ".//button")

    filtered_rooms = []
    filtered_beds = []
    filtered_baths = []

    def filter_noptions(lista1, lista2):
        for element in lista1:
            if not any(val in element.text for val in ["Cualquiera", "5", "6", "7", "8+", "4"]):
                lista2.append(element)
        #for filtered in lista2:
        #    print(filtered.text)
    
    #closebutton = driver.find_element(By.XPATH, '//button[@aria-label="Cerrar"]')
    
    filter_noptions(rooms, filtered_rooms)
    filter_noptions(beds, filtered_beds)
    filter_noptions(baths, filtered_baths)

    random.choice(filtered_rooms).click()
    random.choice(filtered_beds).click()
    random.choice(filtered_baths).click()

    filterbutton = driver.find_element(By.XPATH, '//a[contains(text(), "Mostrar")]')
    time.sleep(1)
    print(''.join(filter(str.isdigit, filterbutton.text)), " elementos encontrados")

    def tipo_filtro(divs):
        options = divs.find_elements(By.XPATH, './div[4]//button')
        #print(len(options))
        buttontipo = random.choice(options)
        buttontipo.click()
        return buttontipo.text

    if int(''.join(filter(str.isdigit, filterbutton.text))) > nfiltro:
        print("Segundo Filtro")
        tipo_vivienda = tipo_filtro(divs)
        print("TIPO SELECCIONADO :  <<< ",tipo_vivienda, " >>>")
        time.sleep(1)
        filterbutton = driver.find_element(By.XPATH, '//a[contains(text(), "Mostrar")]')
        print("Elemtos reducidos a ",''.join(filter(str.isdigit, filterbutton.text)), " objetos")    
    
    def servicio_filtro(divs):
        options = divs.find_elements(By.XPATH, './div[5]//span[@data-checkbox="true"]')
        #print(len(options))
        random.choice(options).click()
        time.sleep(1)
        filterbutton = driver.find_element(By.XPATH, '//a[contains(text(), "Mostrar")]')
        if int(''.join(filter(str.isdigit, filterbutton.text))) > nfiltro:
            print("Filtro Extra")
            servicio_filtro(divs)
    
    if int(''.join(filter(str.isdigit, filterbutton.text))) > nfiltro:
        print("Tercer Filtro")
        button = divs.find_element(By.XPATH, './div[5]//span[contains(text(), "Muestra")]/..')
        button.click()
        time.sleep(2)
        servicio_filtro(divs)
        time.sleep(1)
        filterbutton = driver.find_element(By.XPATH, '//a[contains(text(), "Mostrar")]')
        time.sleep(1)
        print("Elementos reducidos a ",''.join(filter(str.isdigit, filterbutton.text)), " objetos")

    filterbutton.click()

def scrap(driver, link, df):
    googlemap = driver.find_element(By.XPATH, '//h2[contains(text(), "A dónde irás")]')
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'instant', block: 'center'});", googlemap)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@class="gm-style"]//a')))
    time.sleep(10)
            
    Link = {"Link":link}
    print(Link)
    Comuna = {"Comuna": driver.find_element(By.XPATH, '//*[@id="site-content"]/div/div[1]/div[1]/div[1]/div/div/div/div/section/div[2]/div[1]/span/button/span').text}
    Camas = {"Camas": driver.find_element(By.XPATH, '//*[@id="site-content"]/div/div[1]/div[3]/div/div[1]/div/div[1]/div/div/section/.//span[contains(text(), "cama")]').text}
    Baños = {"Baños": driver.find_element(By.XPATH, '//*[@id="site-content"]/div/div[1]/div[3]/div/div[1]/div/div[1]/div/div/section/.//span[contains(text(), "baño")]').text}
    Capacidad = {"Capacidad":driver.find_element(By.XPATH, '//*[@id="site-content"]/div/div[1]/div[3]/div/div[1]/div/div[1]/div/div/section/.//span[contains(text(), "huésped")]').text}
    Habitaciones = {"Habitaciones":driver.find_element(By.XPATH, '//*[@id="site-content"]/div/div[1]/div[3]/div/div[1]/div/div[1]/div/div/section/.//span[contains(text(), "habitacion")]').text}
    try: 
        if driver.find_element(By.XPATH, '//*[@id="site-content"]/div/div[1]/div[3]/div/div[2]/div/div/div[1]/div/div/div/div/div/div/div[1]/div[1]/div[1]/div/span/div/span[2]').text == "noche":
            Precio = {"Precio":driver.find_element(By.XPATH, '//*[@id="site-content"]/div/div[1]/div[3]/div/div[2]/div/div/div[1]/div/div/div/div/div/div/div[1]/div[1]/div[1]/div/span/div/span[1]').text}
        else: Precio = {"Precio":driver.find_element(By.XPATH, '//*[@id="site-content"]/div/div[1]/div[3]/div/div[2]/div/div/div[1]/div/div/div/div/div/div/div[1]/div[1]/div[1]/div/span/div/span[2]').text}
    except: Precio = {"Precio": None}
    try: Nota = {"Nota":driver.find_element(By.XPATH, '//*[@id="site-content"]/div/div[1]/div[3]/div/div[2]/div/div/div[1]/div/div/div/div/div/div/div[1]/div[1]/div[2]/span/span[2]').text}
    except: Nota = {"Nota": None}
    try: Descripcion = {"Descripcion":driver.find_element(By.XPATH, '//*[@data-section-id="DESCRIPTION_DEFAULT"]/div/div/span/span').text}
    except: Descripcion = {"Descripcion":None}
    try: Nnota = {"Nnota":driver.find_element(By.XPATH, '//*[@id="site-content"]/div/div[1]/div[3]/div/div[2]/div/div/div[1]/div/div/div/div/div/div/div[1]/div[1]/div[2]/span/span[3]/button/span').text}
    except: Nnota = {"Nota": None}
    Titulo1 = {"Titulo1":driver.find_element(By.XPATH, '//*[@id="site-content"]/div/div[1]/div[1]/div[1]/div/div/div/div/section/div[1]/span/h1').text}
    Titulo2 = {"Titulo2":driver.find_element(By.XPATH, '//*[@id="site-content"]/div/div[1]/div[3]/div/div[1]/div/div[1]/div/div/section/div/div/div/div[1]/div/h2').text}
    Servicios = {"Servicios":driver.find_element(By.XPATH, '//*[@data-section-id="AMENITIES_DEFAULT"]/section/div[3]/div').text}
    Anfitrion = {"Anfitrion":driver.find_element(By.XPATH, '//*[@id="site-content"]/div/div[1]/div[6]/div/div/div/div[2]/div/section/div[1]/div[2]/h2').text}
    Registro = {"Registro":driver.find_element(By.XPATH, '//*[@id="site-content"]/div/div[1]/div[6]/div/div/div/div[2]/div/section/div[1]/div[2]/div/ol/li').text}
    try: Ubides = {"Ubides":driver.find_element(By.XPATH, '//*[@id="site-content"]/div/div[1]/div[5]/div/div/div/div[2]/div/section/div[4]/div/div/div/div[2]/span/span').text}
    except: Ubides = {"Ubides":None}
    Ubicacion = {"Ubicacion":driver.find_element(By.XPATH, '//*[@class="gm-style"]//a').get_attribute("href")}
    n_free_date = {"n_free_date": driver.find_element(By.XPATH, '//div[contains(text(),"Llegada")]/../div[contains(@data-testid, "change-dates")]').text}
    ScrapDate = {"ScrapDate": datetime.now().date().strftime("%d-%m-%Y")}
    dicts = [Link, Camas, Baños, Capacidad, Habitaciones, Precio, Nota, Nnota,
        Descripcion, Titulo1, Titulo2, Servicios, Anfitrion, Registro, Ubides, Ubicacion, n_free_date, ScrapDate]
    #print(dicts)
    for dic in dicts:
        Comuna.update(dic)

    dfmin = pd.DataFrame([Comuna])
    df = pd.concat([df,dfmin])
    return df

def scrap_items(driver, df):
    print("obteniendo links")
    wait = WebDriverWait(driver, 10)
    print("debug1")
    wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@style, "contents")]/.//div[@itemprop="itemListElement"]/div/div/div/a')))
    print("debug2")
    initial_url = driver.current_url
    print("debug3")
    #print(type(initial_url))
    #print(initial_url)
    items = driver.find_elements(By.XPATH, '//div[contains(@style, "contents")]/.//div[@itemprop="itemListElement"]/div/div/div/a')
    print(len(items))
    links = []
    for item in items:
        #print(item.get_attribute("href"))
        links.append(item.get_attribute("href"))
    if len(links) == 0:
        y = 1
        return df, y
    else:
        for link in links:
            try: 
                driver.get(link)
                #time.sleep(3)
                wait = WebDriverWait(driver, 10)
                wait.until(EC.presence_of_all_elements_located((By.XPATH, '//h2[contains(text(), "A dónde irás")]')))
                df = scrap(driver, link, df)
            except: 
                print("POP UP ACTIVO /// DEMORA EXTRA EN CARGADO")
                time.sleep(6)
                try:
                    time.sleep(1)
                    cerrar_button = driver.find_element(By.XPATH, "//button[@aria-label='Cerrar']")
                    cerrar_button.click()
                    time.sleep(1)
                    df = scrap(driver, link, df)
                except: 
                    try:
                        time.sleep(1)
                        driver.get(link)
                        wait = WebDriverWait(driver, 10)
                        wait.until(EC.presence_of_all_elements_located((By.XPATH, '//h2[contains(text(), "A dónde irás")]')))
                        df = scrap(driver, link, df)
                    except: 
                        print("ITERATION KILLER ERROR, FINALIZANDO")
                        y = 1

    driver.get(initial_url)
    time.sleep(5)
    print(len(links), "CONTROL PREVIO A NEXTPAGE")
    df, y = siguiente_pag(driver, df)
    return df, y

def siguiente_pag(driver, df):
    try: 
        button = driver.find_element(By.XPATH, '//*[@aria-label="Siguiente"]')
        print("Cargando siguiente página")
        time.sleep(5)
        linkbut = button.get_attribute("href")
        print("Link CARGANDO", button.get_attribute("href"))
        button.click()
        if linkbut == None:
            y = 1
            return df, y 
        df, y = scrap_items(driver, df)
        return df, y
    except: 
        y = 1
        return df,y

def pre_procesado(df):
    print("debug01")
    dfpre = df.copy(True)
    print("debug02")
    def get_region(comuna):
        parts = comuna.split(',')
        return parts[1].strip() if len(parts) > 1 else None
    dfpre['Region'] = df['Comuna'].apply(get_region)
    print("debug03")
    dfpre['Comuna'] = df['Comuna'].apply(lambda x: x.split(',')[0])
    print("debug")
    dfpre["Camas"] = df["Camas"].apply(lambda x:x.replace(" ","").replace("camas","").replace("cama",""))
    print("debug")
    dfpre["Baños"] = df["Baños"].apply(lambda x:x.replace(" ","").replace("baños","").replace("baño",""))
    print("debug")
    dfpre["Tipo_Baños"] = df["Baños"].apply(lambda x: 'compartido' if 'compartido' in x else 'privado')
    print("debug")
    dfpre["Capacidad"] = df["Capacidad"].apply(lambda x:x.replace(" huéspedes","").replace(" huésped",""))
    print("debug")
    def remove_numbers(input_string):
        return input_string.translate(str.maketrans("", "", string.digits))
    dfpre["Habitaciones"] = df["Habitaciones"].apply(remove_numbers)
    print("debug 1")
    dfpre["Habitaciones"] = dfpre["Habitaciones"].apply(lambda x:x.replace("habitaciones","Habitación"))
    print("debug2")
    dfpre["N_Habitaciones"] = df["Habitaciones"].apply(lambda x: '1' if 'Estudio' in x else x.replace(" habitaciones","").replace(" habitación",""))
    print("debug3")
    #dfpre["Precio"] = df["Precio"].apply(lambda x: x if x is None else x.replace(" CLP","").replace("$","").replace(",",""))
    #dfpre["Precio"] = dfpre["Precio"].apply(lambda x: None if x is None else x.extract(r'(\d+(?:,\d+)?)'))
    dfpre["Precio"] = df["Precio"].fillna('0')
    print("debug4")
    dfpre["Precio"] = dfpre["Precio"].str.extract(r'(\d+(?:,\d+)?)')
    print("debug5")
    dfpre["Precio"] = dfpre["Precio"].str.replace(',', '.')
    print("debug6")
    dfpre["Precio"] = dfpre["Precio"].astype(float)
    print("debug7")
    dfpre["Nota"] = df["Nota"].apply(lambda x: x if x is None else x.replace(" ·", ""))
    print("debug8")
    dfpre["Nnota"]  = df["Nnota"].apply(lambda x: str(x).replace(" reseñas", "").replace(" reseña","") if not pd.isnull(x) else x)
    print("debug9")
    dfpre["Titulo2"] = df['Titulo2'].apply(lambda x: x.split(' - ')[0])
    print("debug10")
    dfpre["Servicios"] = df["Servicios"].apply(lambda x: x.split(' - '))
    print("debug11")
    dfpre["Anfitrion"] = df["Anfitrion"].apply(lambda x:x.replace("Anfitrión: ",""))
    print(df.shape)
    print(dfpre.shape)
    dfpre["Registro"] = df["Registro"].apply(lambda x:x.replace("Se registró en ","").replace(" de ","-"))
    print("debug12")
    def transform_string(s):
        months = {
        "enero": "01",
        "febrero": "02",
        "marzo": "03",
        "abril": "04",
        "mayo": "05",
        "junio": "06",
        "julio": "07",
        "agosto": "08",
        "septiembre": "09",
        "octubre": "10",
        "noviembre": "11",
        "diciembre": "12"
        }
        month, year = s.split("-")
        return f"{months[month]}-{year}"
    print("debug")
    dfpre["Registro"] = dfpre["Registro"].apply(transform_string)
    print("debug")
    dfpre[["lat", "lon"]] = df["Ubicacion"].str.extract(r"ll=(-\d+\.\d+),(-\d+\.\d+)")
    print("debug")
    cols = ['Titulo1', 'Titulo2', 'Comuna', 'Region', 'Capacidad',  'Camas', 'N_Habitaciones', 'Habitaciones', 'Baños',  'Tipo_Baños', 'Precio',  'lat', 'lon', 'Ubicacion', 'Ubides', 'Descripcion', 'Servicios', 'Nota', 'Nnota', 'Anfitrion', 'Registro', 'Link']
    dfpre = dfpre[cols].reset_index()
    print("debug")
    dfpre = dfpre.drop('index', axis=1)
    print("debug")
    return dfpre

""" FLUJO DE TRABAJO 

- Creación de 

"""

busqueda = "Coquimbo Region, Chile"
df = pd.DataFrame()
y = 0
iter = 264
iterfin = 350
nfiltro = 500

folderpath = create_folders()

while iter<iterfin:
    try:
        df = pd.DataFrame()
        driver = opendriver(options)
        apertura_marketplace(driver, busqueda)
        aplicar_filtros(driver, nfiltro)
        time.sleep(3)
        print("FILTROS APLICADOS")
        print("y = ", y)
        while y == 0:
            df, y = scrap_items(driver, df)
        print("debug x")
        dfpre = pre_procesado(df)

        dfpre.to_csv(os.path.join(folderpath, f"{busqueda}{iter}.csv"))
        driver.quit()
        y = 0
        iter+=1
    except: continue