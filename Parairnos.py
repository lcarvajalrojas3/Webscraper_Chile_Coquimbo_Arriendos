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
import re

def create_folders(busqueda, iter):
    print("\n\nRevisando existencia de carpetas necesarias")
    dir_path = os.path.dirname(os.path.realpath("__file__"))
    print("path local: ", dir_path)
    folderpath = "Parairnos"
    folderpath = os.path.join(dir_path, folderpath)
    if not os.path.exists(folderpath):
        os.mkdir(folderpath)
        print("Carpeta Parairnos creada")
    else: print("Carpeta Parairnos existente")
    dir_path = folderpath
    folderpath = f"Data_porpag_{busqueda}_{iter}"
    folderpath = os.path.join(dir_path, folderpath)
    if not os.path.exists(folderpath):
        os.mkdir(folderpath)
        print("Subcarpeta Data creada\n\n")
    else: print("Subcarpeta Data Existente")
    return folderpath, dir_path

options = Options()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument("--disable-notifications")

def opendriver(options):
    driver = webdriver.Chrome(options=options)
    time.sleep(2)
    driver.maximize_window()
    print("Abriendo WebDriver")
    time.sleep(2)
    return driver

def apertura_portal(driver, busqueda):
    url = "https://www.parairnos.cl/"
    driver.get(url)
    time.sleep(3)
    print("Cargando Página y realizando búsqueda de '", busqueda, "'")
    buscador = driver.find_element(By.XPATH,'//*[@id="parairnosSearch"]')
    buscador.click()
    buscador.send_keys(Keys.CONTROL, "a")
    buscador.send_keys(Keys.DELETE)
    time.sleep(1)
    #buscador = driver.find_el ement(By.XPATH, '//input[@id="bigsearch-query-location-input"]')
    #buscador.clear()   ]
    buscador.send_keys(busqueda)
    button = driver.find_elements(By.XPATH,'//button[@type="submit"]')
    button[1].click()
    time.sleep(3)

def scrap(driver, link, df, dfpage):
    driver.get(link)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="parairnos-google-maps"]')))
    #time.sleep(3)
    googlemap = driver.find_element(By.XPATH, '//div[@class="parairnos-google-maps"]')
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'instant', block: 'center'});", googlemap)
    #time.sleep(4)
    wait = WebDriverWait(driver, 10)
    try: wait.until(EC.presence_of_all_elements_located((By.XPATH, '//span[@class="fa-bed"]/..')))
    except: pass

    Link = {"Link":link}
    print(Link)
    Comuna = {"Comuna": driver.find_element(By.XPATH, '//span[@itemprop="addressLocality"]').text}
    #print(Comuna)

    Region = {"Region": driver.find_element(By.XPATH, '//span[@itemprop="addressRegion"]').text}
    #print(Region)

    try:
        infocamas = driver.find_element(By.XPATH, '//span[@class="fa-bed2"]/..').text
        numbers = re.findall(r'\d+', infocamas)
        max_number = max(map(int, numbers))
        Camas = {"Camas": max_number}
    except: Camas = {"Camas": None}
    #print(Camas)

    try: Baños = {"Baños": ''.join(filter(str.isdigit, driver.find_element(By.XPATH, '//span[@class="fa-bath"]/..').text))}
    except: Baños = {"Baños": None}
    #print(Baños)

    try: Capacidad = {"Capacidad": max_number}
    except: Capacidad = {"Capacidad": None}
    #print(Capacidad)
    
    try: Habitaciones = {"Habitaciones": ''.join(filter(str.isdigit, driver.find_element(By.XPATH, '//span[@class="fa-bed"]/..').text))}
    except: Habitaciones = {"Habitaciones": None}
    #print(Habitaciones)

    infoprecio = ''.join(filter(str.isdigit, driver.find_element(By.XPATH, '//span[@class="price"]').text))
    if infoprecio == "":
        infoprecio = None
    Precio = {"Precio": infoprecio}
    #print(Precio)
    
    try: Nota = {"Nota":driver.find_element(By.XPATH, '//*[@id="userComments"]/div[1]/div/div/div[2]/div[1]').text}
    except: Nota = {"Nota": None}
    #print(Nota)

    try: Nnota = {"Nnota":''.join(filter(str.isdigit, driver.find_element(By.XPATH, '//*[@id="userComments"]/div[1]/div/div/div[2]/div[3]').text))}
    except: Nnota = {"Nota": None}
    #print(Nnota)

    try: 
        info_comentarios = driver.find_elements(By.XPATH, '//*[@id="userComments"]/div[2]/div/div/div/div/p')
        comentarios = []
        for item in info_comentarios:
            comentarios.append(item.text)
        Comentarios = {"Comentarios": comentarios}
    except: {"Comentarios": None}
    #print(Comentarios)

    try: Descripcion = {"Descripción":driver.find_element(By.XPATH, '//div[@itemprop="description"]').text.replace("\n", " ")}
    except: Descripcion = {"Descripción":None}
    #print(Descripcion)

    Titulo1 = {"Titulo1":driver.find_element(By.XPATH, '//h1[@itemprop="name"]').text}
    #print(Titulo1)
    
    try: 
        info_servicios = driver.find_elements(By.XPATH, '//h4[contains(text(), "Características")]/../div/div/div/ul/li')
        servicios = []
        for item in info_servicios:
            servicios.append(item.text)
        Servicios = {"Servicios": servicios}
    except: Servicios = {"Servicios": None}
    #print(Servicios)
    
    info_anfitrion = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div[2]/aside/div[3]/div/div/div[2]/h4').text.split("\n")
    Anfitrion = {"Anfitrion":info_anfitrion[0]}
    #print(Anfitrion)

    Tipo_Anfitrion = {"Tipo_Anfitrion":info_anfitrion[1]}
    #print(Tipo_Anfitrion)
    
    Registro = {"Registro":driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div[2]/aside/div[3]/div/div/div[2]/p[3]/strong').text}
    #print(Registro)

    Telefono = {"Telefono": driver.find_element(By.XPATH, '//div[@class="description-phone"]/../div/a').text}
    #print(Telefono)

    info_direccion = driver.find_element(By.XPATH, '//span[@itemprop="address"]').text.split(", ")
    Direccion = {"Direccion": info_direccion[0] + ", " + info_direccion[1]}
    #print(Direccion)
    
    Ubicacion = {"Ubicacion":driver.find_element(By.XPATH, '//div[@class="parairnos-google-maps"]/iframe').get_attribute("src")}
    #print(Ubicacion)

    info_ubicacion = driver.find_element(By.XPATH, '//div[@class="parairnos-google-maps"]/iframe').get_attribute("src")
    lat = {"lat": re.findall(r"-\d+\.\d+", info_ubicacion)[0]}
    long =  {"long": re.findall(r"-\d+\.\d+", info_ubicacion)[1]}
    #print(lat, long)

    #n_free_date = {"n_free_date": driver.find_element(By.XPATH, '//div[contains(text(),"Llegada")]/../div[contains(@data-testid, "change-dates")]').text}
    

    ScrapDate = {"ScrapDate": datetime.now().date().strftime("%d-%m-%Y")}
    
    dicts = [Link, Region, Camas, Baños, Capacidad, Habitaciones, Precio, Nota, Nnota, Comentarios, 
        Descripcion, Titulo1, Servicios, Anfitrion, Tipo_Anfitrion, Registro, Telefono, Direccion, Ubicacion, lat, long, ScrapDate]
    
    #print(dicts)
    for dic in dicts:
        Comuna.update(dic)

    dfmin = pd.DataFrame([Comuna])
    dfpage = pd.concat([dfpage, dfmin])
    df = pd.concat([df,dfmin])
    return df, dfpage

def scrap_links(driver, df, pag, folderpath):
    initial_url = driver.current_url
    #print(type(initial_url))
    #print(initial_url)
    items = driver.find_elements(By.XPATH, '//div[@class="results-content"]/div/a[@itemprop="url"]')
    print(len(items))
    links = []
    dfpage = pd.DataFrame()
    for item in items:
        #print(item.get_attribute("href"))
        links.append(item.get_attribute("href"))

    for link in links:
        #print(link)
        df, dfpage = scrap(driver, link, df, dfpage)

    driver.get(initial_url)
    dfpage.to_csv(os.path.join(folderpath, f"Data_{pag}"))
    pag = pag + 1
    return df, pag

def siguiente_pagina(driver):
    button = driver.find_element(By.XPATH, '//ul[contains(@class, "pagination")]/li[last()]/a')
    print("Cargando siguiente página")
    #time.sleep(5)
    linkbut = button.get_attribute("href")
    #print("Link CARGANDO", button.get_attribute("href"))
    #if button.is_enabled():
    if linkbut != None:
        button.click()
        y = 0
        return y
    else: 
        print("NO HAY SIGUIENTE PÁGINA")
        y = 1
        return y


""" FLUJO """

busqueda = "Coquimbo"
pag = 1
iter = 1
df = pd.DataFrame()
y = 0

folderpath, dir_path = create_folders(busqueda, iter)

driver = opendriver(options)
apertura_portal(driver, busqueda)

while y == 0:
    df, pag = scrap_links(driver, df, pag, folderpath)
    y = siguiente_pagina(driver)

df.to_csv(os.path.join(folderpath, f"Total_Data_{busqueda}_{iter}"))