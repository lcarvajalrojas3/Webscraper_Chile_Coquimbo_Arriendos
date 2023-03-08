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

"""
FLUJO DE TRABAJO

CREACIÓN DE CARPETAS DE GUARDADO

APERTURA DE DRIVER
LOGIN DE CUENTA
APERTURA MARKETPLACE
BÚSQUEDA EN MARKETPLACE

SCRAP DE DATA
    - SCROLL DOWN
    - DATA SCRAPP
    - GUARDADO DE CSV*SCROLL

UNIÓN DE DFs

"""

def create_folders(busqueda, iter):
    print("\n\nRevisando existencia de carpetas necesarias")
    dir_path = os.path.dirname(os.path.realpath(__file__))
    print("path local: ", dir_path)
    folderpath = "Marketplace"
    folderpath = os.path.join(dir_path, folderpath)
    if not os.path.exists(folderpath):
        os.mkdir(folderpath)
        print("Carpeta Marketplace creada")
    else: print("Carpeta Marketplace existente")
    dir_path = folderpath
    folderpath = f"Data_{busqueda}_{iter}"
    folderpath = os.path.join(dir_path, folderpath)
    if not os.path.exists(folderpath):
        os.mkdir(folderpath)
        print("Subcarpeta Data creada\n\n")
    else: print("Subcarpeta Data Existente")
    return folderpath

def opendriver(options):
    print("\nIniciando proceso de SCRAPPING\n")
    driver = webdriver.Chrome(options=options)
    time.sleep(2)
    driver.maximize_window()
    print("\nAbriendo WebDriver \n")
    time.sleep(2)   
    return driver

def login(driver, mail, clave):
    loginurl = "https://es-la.facebook.com/"
    driver.get(loginurl)
    print("Cargando página de Log-in")
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*')))
    time.sleep(3)

    driver.find_element(By.XPATH,'//*[@id="email"]').click()
    driver.find_element(By.XPATH,'//*[@id="email"]').clear()
    driver.find_element(By.XPATH,'//*[@id="email"]').send_keys(mail)

    driver.find_element(By.XPATH,'//*[@id="pass"]').click()
    driver.find_element(By.XPATH,'//*[@id="pass"]').clear()
    driver.find_element(By.XPATH,'//*[@id="pass"]').send_keys(clave)

    driver.find_element(By.XPATH,'//*[@name="login"]').click()
    time.sleep(1)
    print("Cuenta Logueada\n")
    time.sleep(2)

def apertura_marketplace(driver, busqueda):
    #marketurl = "https://www.facebook.com/marketplace/105686679466017/search/?query=arriendo"
    marketurl = "https://www.facebook.com/marketplace/111140098911364"
    driver.get(marketurl)
    time.sleep(3)
    print("Cargando Marketplace y realizando búsqueda de '", busqueda, "'")
    buscador = driver.find_element(By.XPATH,'//input[@aria-label="Buscar en Marketplace"]')
    buscador.click()
    #buscador.clear()
    buscador.send_keys(Keys.CONTROL, "a")
    buscador.send_keys(Keys.DELETE)
    buscador.send_keys(busqueda)
    buscador.send_keys(Keys.RETURN)
    time.sleep(2)

def carga_scroll(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    print("Scroll down realizado")
    time.sleep(4)
    #roads = driver.find_elements(By.XPATH,'//*/div/div[1]/div/div[5]/div/div/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div[3]/div/div[2]/div')
    roads = driver.find_elements(By.XPATH,'//div/*[contains(@style, "max-width: 381px; min-width: 242px;")]')
    initial = 0
    print(len(roads), "elementos localizados\n\n")
    return roads, initial

def scrapvar(driver, dfpag):
    print("scrapvar ----- scrapvar --------- scrapvar")
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@href,'profile')]/span")))
    time.sleep(random.randint(15, 40))
    profile = driver.find_elements(By.XPATH,"//a[contains(@href,'profile')]/span")[1].text
    print(profile)
    Link = driver.current_url
    print(Link)
    try: 
        description_button = driver.find_element(By.XPATH,"//span[contains(text(), 'Ver más')]")
        description_button.click()
    except: pass
    try: description = driver.find_element(By.XPATH,"//*/div/div[1]/div/div[5]/div/div/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div/div/div/div[2]/div/div[2]/div/div[1]/div[1]/div[8]/div[2]/div/div/div/span").text
    except: 
        try: description = driver.find_element(By.XPATH, "//*/div/div[1]/div/div[7]/div/div/div[3]/div[2]/div/div[2]/div/div[2]/div/div[2]/div[1]/div[8]/div[2]/div/div/div/span").text
        except: description = None
    try: print(description) 
    except: pass
    try:precio = driver.find_element(By.XPATH, "//span[contains(text(), '/mes')]")
    except: precio = driver.find_element(By.XPATH, "//div/div/span[contains(text(), '/mes') or contains(text(), '$')]")
    if precio.text == "GRATIS/mes":
        precio = None
    else:
        try:
            precio, resto = precio.text.replace("/mes","").replace("$","").replace(".","").split("\n")
            precio = float(precio)
            print(precio)
        except: 
            precio = precio.text.replace("/mes","").replace("$","").replace(".","")
            print(precio)
    try:
        Direccion, Comuna, Region = driver.find_element(By.XPATH, "//*/div/div[1]/div/div[5]/div/div/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div/div/div/div[2]/div/div[2]/div/div[1]/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div/span").text.split(", ")
        print(Direccion, Comuna, Region, 1)
    except:
        try: 
            Comuna, Region = driver.find_element(By.XPATH, "//*/div/div[1]/div/div[5]/div/div/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div/div/div/div[2]/div/div[2]/div/div[1]/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div/span").text.split(", ")
            print(Comuna, Region, 2)
            Direccion = None
        except: 
            try:
                Direccion, Comuna, Region = driver.find_element(By.XPATH,"//*/div/div[1]/div/div[7]/div/div/div[3]/div[2]/div/div[2]/div/div[2]/div/div[2]/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div/span").text.split(", ")
                print(Direccion, Comuna, Region, 3)
            except: 
                try: 
                    t = driver.find_element(By.XPATH, "//span[contains(text(), 'La ubicación')]")
                    #print(t.text)
                    t = t.find_element(By.XPATH, "../../..")
                    Comuna, Region = t.find_element(By.XPATH, "div[1]").text.split(", ")
                    print(Comuna, Region)
                    Direccion = None
                except:
                    Comuna, Region, Direccion = None, None, None #### AQUI HAY UN PROBLEMA
                    print("COMUNA NO ENCONTRADA")
    #try: print(Direccion)
    #except: pass
    #print(Comuna)
    #print(Region)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_all_elements_located((By.XPATH, "//*/div/h1")))
    try: 
        Titulo = driver.find_element(By.XPATH, "//*/div/div[1]/div/div[5]/div/div/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div/div/div/div[2]/div/div[2]/div/div[1]/div[1]/div[1]/h1").text
    except: 
        Titulo = driver.find_elements(By.XPATH, "//*/div/h1")
        Titulo = Titulo[0].text
    print(Titulo)
    try: 
        latlong = driver.find_element(By.XPATH, "//div[contains(@style,'url')]")
        ubi = latlong.get_attribute("style")
        start = ubi.index("&center=")
        end = ubi.index("&marker_list")
        lat_long = ubi[start+8:end]
        lat, long = lat_long.split("%2C")
    except: 
        latlong = driver.find_element(By.XPATH, "//div[contains(@style,'url')]")
        ubi = latlong.get_attribute("style")
        start = ubi.index("&center=")
        end = ubi.index("&circle")
        lat_long = ubi[start+8:end]
        lat, long = lat_long.split("%2C")
    #lat_long = [ubi[start+8:end]]
    print(lat)
    print(long)
    #try: Detallespre = driver.find_elements(By.XPATH, "//*/div/div[1]/div/div[5]/div/div/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div/div/div/div[2]/div/div[2]/div/div[1]/div[1]/div[6]/div")
    try:
        Detallespre = driver.find_element(By.XPATH, "//*/span[contains(text(), 'Detalles de la unidad')]")
        Detallespre = Detallespre.find_element(By.XPATH, "../../../../../../../..")
        Detallespre = Detallespre.find_elements(By.XPATH, "././././././*")
        Detalles = []
        #print(Detallespre)

        for detail in Detallespre:
            #print(detail.text)
            Detalles.append(detail.text)
        print(Detalles)
    except: Detalles = None


    Scrapdate = datetime.now().date().strftime("%d-%m-%Y")
    dicc = {"Link":Link, "Anfitrion": profile, "Descripcion": description, "Precio": precio, "Direccion": Direccion, "Comuna":Comuna, "Region": Region, 
            "Titulo1":Titulo, "lat":lat, "long": long, "Detalles": Detalles, "ScarpDate": Scrapdate}
    print("dicc exitoso")
    dfitem = pd.DataFrame([dicc])
    dfpag = pd.concat([dfpag, dfitem])
    return dfpag

def info_scrap(driver, initial, roads, folderpath):
    print("Obteniendo datos desde el objeto ", initial+1, " al ", len(roads))
    dfpag = pd.DataFrame()
    time.sleep(random.randint(10, 15))
    try: 
        for n in range (initial,len(roads)+1,1):
            print("\nItem ", initial+1, " de ", len(roads))
            time.sleep(random.randint(10, 30))
            if roads[n].find_elements(By.XPATH,"./child::*//*[contains(text(), 'Publicidad')]"):
                print("publicidad en Item", initial+1)
                initial +=1
            else:
                print("Aviso efectivo en Item ", initial+1)
                roads[n].click()
                time.sleep(random.randint(10, 15))
                wait = WebDriverWait(driver, 10)
                wait.until(EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@href,'profile')]/span")))
                #time.sleep(3)
                try:
                    profile = driver.find_elements(By.XPATH,"//a[contains(@href,'profile')]/span")[1].text
                    print(profile)
                    Link = driver.current_url
                    print(Link)
                    try: 
                        description_button = driver.find_element(By.XPATH,"//span[contains(text(), 'Ver más')]")
                        description_button.click()
                    except: pass
                    try: description = driver.find_element(By.XPATH,"//*/div/div[1]/div/div[7]/div/div/div[3]/div[2]/div/div[2]/div/div[2]/div/div[2]/div[1]/div[8]/div[2]/div/div/div/span").text
                    except: description = driver.find_element(By.XPATH,"//*/div/div[1]/div/div[7]/div/div/div[3]/div[2]/div/div[2]/div/div[2]/div/div[2]/div[1]/div[1]/div[5]/div/div[2]/div[1]/div/span").text
                    try: precio = driver.find_element(By.XPATH, "//span[contains(text(), '/mes')]")
                    except: precio = driver.find_element(By.XPATH, "//*/div/div[1]/div/div[7]/div/div/div[3]/div[2]/div/div[2]/div/div[2]/div/div[2]/div[1]/div[1]/div[1]/div[1]/div/span")
                    if precio.text == "GRATIS/mes":
                        precio = None
                    else:
                        print(precio.text)
                        print(float(precio.text.replace("/mes","").replace("$","").replace(".","")))
                        precio = float(precio.text.replace("/mes","").replace("$","").replace(".",""))
                    try: Comuna, Region = driver.find_element(By.XPATH, "//*/div/div[1]/div/div[7]/div/div/div[3]/div[2]/div/div[2]/div/div[2]/div/div[2]/div[1]/div[7]/div[3]/div/div[1]/span").text.split(", ")
                    except: Comuna, Region = driver.find_element(By.XPATH, "//*/div/div[1]/div/div[7]/div/div/div[3]/div[2]/div/div[2]/div/div[2]/div/div[2]/div[1]/div[1]/div[1]/div[2]/div/div/span/a/span").text.split(", ")
                    #print(Comuna)
                    #print(Region)
                    try: Titulo = driver.find_element(By.XPATH, "//*/div/div[1]/div/div[7]/div/div/div[3]/div[2]/div/div[2]/div/div[2]/div/div[2]/div[1]/div[1]/h1").text
                    except: Titulo = driver.find_element(By.XPATH, "//*/div/div[1]/div/div[7]/div/div/div[3]/div[2]/div/div[2]/div/div[2]/div/div[2]/div[1]/div[1]/div[1]/h1").text
                    print(Titulo)
                    try: latlong = driver.find_element(By.XPATH, "//*/div/div[1]/div/div[7]/div/div/div[3]/div[2]/div/div[2]/div/div[2]/div/div[2]/div[1]/div[7]/div[2]/div/div[1]/div/div/div[1]")
                    except: latlong = driver.find_element(By.XPATH, "//*/div/div[1]/div/div[7]/div/div/div[3]/div[2]/div/div[2]/div/div[2]/div/div[2]/div[1]/div[1]/div[5]/div/div[2]/div[3]/div[1]/div/div/div/div[1]")
                    ubi = latlong.get_attribute("style")
                    start = ubi.index("&center=")
                    end = ubi.index("&circle=")
                    lat_long = ubi[start+8:end]
                    lat, long = lat_long.split("%2C")
                    #lat_long = [ubi[start+8:end]]
                    #print(lat)
                    #print(long)
                    Scrapdate = datetime.now().date().strftime("%d-%m-%Y")
                    dicc = {"Link":Link, "Anfitrion": profile, "Descripcion": description, "Precio": precio, "Comuna":Comuna, "Region": Region, "Titulo1":Titulo, "lat":lat, "long": long, "ScarpDate": Scrapdate}
                    dfitem = pd.DataFrame([dicc])
                    dfpag = pd.concat([dfpag, dfitem])
                    initial += 1
                except: 
                    dfpag = scrapvar(driver, dfpag)
                    initial += 1

                close_button = driver.find_element(By.XPATH,'//div[@aria-label="Cerrar"]')
                close_button.click()
                #time.sleep(2)
    except:
        time.sleep(3)
        try:
            close_button = driver.find_element(By.XPATH,'//div[@aria-label="Cerrar"]')
            close_button.click()
        except:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            roads = driver.find_elements(By.XPATH,'//div/*[contains(@style, "max-width: 381px; min-width: 242px;")]')    
            if initial == len(roads):
                        print("TÉRMINO DE SCRIPT")
                        print(initial)
                        print(len(roads))
                        dfcheck = dfpag
                        dfcheck.to_csv(os.path.join(folderpath,f"Dfcheck_{initial}.csv"))
                        return print("TOPE INFERIOR ALCANZADO")
            else: 
                dfcheck = dfpag
                dfcheck.to_csv(os.path.join(folderpath,f"Dfcheck_{initial}.csv"))
                #roads = driver.find_elements(By.XPATH,'//*/div/div[1]/div/div[5]/div/div/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div[3]/div/div[2]/div')
                roads = driver.find_elements(By.XPATH,'//div/*[contains(@style, "max-width: 381px; min-width: 242px;")]')
                info_scrap(driver, initial, roads, folderpath)   

def driver_quit(driver):
    driver.quit()
    print("DRIVER CERRADO")

def union_dfs(folderpath, iter, busqueda):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    files = os.listdir(folderpath)
    print(files)

    paths = []
    for file in files:
        path = os.path.join(folderpath, file)
        if os.path.isfile(path):
            paths.append(path)

    df = pd.DataFrame()
    for file in paths:
        dftemp = pd.read_csv(file)
        df = pd.concat([df, dftemp])

    df.to_csv(os.path.join(dir_path,"Marketplace",f"Df_Total_{busqueda}_{iter}.csv"))
    print("DF DE ITERACIÓN CREADO -----------------------------------------")

def df_total():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    files = os.listdir(os.path.join(dir_path,"Marketplace"))
    print("UNIENDO DFs: ", len(files), " encontrados : ")
    print(files)

    paths = []
    for file in files:
        path = os.path.join(folderpath, file)
        if os.path.isfile(path):
            paths.append(path)

    df = pd.DataFrame()
    for file in paths:
        dftemp = pd.read_csv(file)
        df = pd.concat([df, dftemp])

    df.to_csv(os.path.join(dir_path,"Marketplace","Df_Total.csv"))
    print("DF DE FINAL CREADO -----------------------------------------")


options = Options()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument("--disable-notifications")
options.add_argument("--incognito")


"""
FLUJO DE TRABAJO

CREACIÓN DE CARPETAS DE GUARDADO

APERTURA DE DRIVER
LOGIN DE CUENTA
APERTURA MARKETPLACE
BÚSQUEDA EN MARKETPLACE

SCRAP DE DATA
    - SCROLL DOWN
    - DATA SCRAPP
    - GUARDADO DE CSV*SCROLL

UNIÓN DE DFs

"""

mail = "Bigdataulsproyect1@gmail.com"
clave = "bigdatauls@1"
busqueda = "arriendo"
iter = 1

#PROXY = "18.212.74.224:3128"  
#options.add_argument('--proxy-server=%s' % PROXY)

for n in range(iter,45,1):
    iter = n
    driver = opendriver(options)
    folderpath = create_folders(busqueda, iter)
    login(driver, mail, clave)
    apertura_marketplace(driver, busqueda)
    roads, initial = carga_scroll(driver)
    info_scrap(driver, initial, roads, folderpath)
    driver_quit(driver)
    union_dfs(folderpath, iter, busqueda)
    df_total() 

    ## 7 -> Carito del pilar astudillo