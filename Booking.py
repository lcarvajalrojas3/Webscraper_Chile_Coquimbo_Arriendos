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

options = Options()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument("--disable-notifications")

def create_folders(iter):
    print("\n\nRevisando existencia de carpetas necesarias")
    dir_path = os.path.dirname(os.path.realpath(__file__))
    print("path local: ", dir_path)
    folderpath = "Booking"
    folderpath = os.path.join(dir_path, folderpath)
    if not os.path.exists(folderpath):
        os.mkdir(folderpath)
        print("Carpeta Booking creada")
    else: print("Carpeta Booking existente")
    dir_path = folderpath
    folderpath = f"Data_porpag_{iter}"
    folderpath = os.path.join(dir_path, folderpath)
    if not os.path.exists(folderpath):
        os.mkdir(folderpath)
        print("Subcarpeta Data creada\n\n")
    #else: print("Subcarpeta Data Existente")
    return folderpath, dir_path

def opendriver(options):
    driver = webdriver.Chrome(options=options)
    time.sleep(2)
    driver.maximize_window()
    print("Abriendo WebDriver")
    time.sleep(2)
    return driver

def apertura_marketplace(driver):
    url = "https://www.booking.com/searchresults.es.html?aid=304142&label=gen173nr-1FCAEoggI46AdIM1gEaC-IAQGYAQq4ARfIAQzYAQHoAQH4AQ2IAgGoAgO4AvaLoJ8GwAIB0gIkZTdlMzVlZWItNjFlYi00MGI3LThiOTUtYzI3NTY2YTZmNzEz2AIG4AIB&sid=f66f439f510c490173e2f538c8f7dfc0&sb=1&sb_lp=1&src=region&src_elem=sb&error_url=https%3A%2F%2Fwww.booking.com%2Fregion%2Fcl%2Fcoquimbo.es.html%3Faid%3D304142%26label%3Dgen173nr-1FCAEoggI46AdIM1gEaC-IAQGYAQq4ARfIAQzYAQHoAQH4AQ2IAgGoAgO4AvaLoJ8GwAIB0gIkZTdlMzVlZWItNjFlYi00MGI3LThiOTUtYzI3NTY2YTZmNzEz2AIG4AIB%26sid%3Df66f439f510c490173e2f538c8f7dfc0%26&ss=Coquimbo+Region&is_ski_area=0&ssne=Coquimbo+Region&ssne_untouched=Coquimbo+Region&region=1352&checkin_year=&checkin_month=&checkout_year=&checkout_month=&efdco=1&group_adults=2&group_children=0&no_rooms=1&b_h4u_keep_filters=&from_sf=1"
    driver.get(url)
    time.sleep(3)

def scrap(driver, link, df, folderpath, pag, dfpage):
    driver.get(link)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="maxotelRoomArea"]/section/div/div[1]')))
    
    ## Scrolldown
    #googlemap = driver.find_element(By.XPATH, '//h2[contains(text(), "A dónde irás")]')
    #driver.execute_script("arguments[0].scrollIntoView({behavior: 'instant', block: 'center'});", googlemap)
    
    time.sleep(1)
    try: 
        datebut = driver.find_element(By.XPATH, '//*[@id="basiclayout"]/div[1]/div[2]/div/div/div[1]/div[1]/div[1]/div[2]/a')
        datebut.click()
    except: 
        print("")
            
    Link = {"Link":link}
    print(Link)
    
    direccion = driver.find_element(By.XPATH, '//span[contains(@class, "address_subtitle")]').text
    Direccion = {"Direccion": direccion}
    #print(Direccion)

    pattern = re.compile(r"\d+")
    # Replace all numeric values in the text with an empty string:
    text_without_numbers = re.sub(pattern, "", direccion.split(",")[1])
    Comuna = {"Comuna": text_without_numbers.strip()}    
   # print(Comuna)
        
    #<<<Baños = {"Baños": driver.find_element(By.XPATH, '//*[@id="site-content"]/div/div[1]/div[3]/div/div[1]/div/div[1]/div/div/section/div/div/div/div[1]/ol/li[4]/span[2]').text}

    datos_seccion = driver.find_element(By.XPATH, '//*[@id="maxotelRoomArea"]/section')
    #print(datos_seccion.text)
    text = datos_seccion.text

    # Use the following pattern to match the required information:
    # (\d+) (cama|camas|litera|literas)
    pattern = re.compile(r"(\d+) (cama individual|camas individuales|cama doble|camas dobles|litera|literas|sofá cama)")
    # Find all matches in the text:
    matches = re.findall(pattern, text)
    camas = []
    bed_count = 0
    # Print the matches:
    for match in matches:
        camas.append(match[0]+" "+match[1])
        #print("MATCH ", match)
        # Check if the bed type is a double bed
        if match[1] in ['cama doble', 'camas dobles', 'litera', 'literas']:
            bed_count += 2 * int(match[0])
        # Check if the bed type is a single bed
        elif match[1] in ['cama individual', 'camas individuales', 'futón']:
            bed_count += int(match[0])
        # Check if the bed type is a sofa bed
        elif match[1] == 'sofá cama':
            bed_count += int(match[0])
    #print("texto extraído", camas)
    #print("bedcount", bed_count)
    

    Camas = {"Camas": bed_count}
    Capacidad = {"Capacidad": bed_count}
    
    divshabit = driver.find_elements(By.XPATH, '//*[@id="maxotelRoomArea"]/section/div/div[1]')
    #print(divshabit)
    #print("items divshabit", len(divshabit))
    infohabits = {}
    for n in range(1,int(len(divshabit)-1),1):
        #print("for", n)
        key = divshabit[n].find_element(By.XPATH, './div[1]').text
        content = divshabit[n].find_element(By.XPATH, './div[2]').text
        dictemp = {key:content}
        infohabits.update(dictemp)
    #print(infohabits)
    info_habitaciones = {"Info_Habitaciones":infohabits}
    ### >> Tipo            
    
    infohabitaciones = driver.find_elements(By.XPATH, '//*[@id="maxotelRoomArea"]/section/div')
    #print(len(infohabitaciones)-1)
    infohabitaciones2 = driver.find_elements(By.XPATH, '//*[@id="maxotelRoomArea"]/section/div/div[1]/div[2]/div')
    nnohabt = 0
    for item in infohabitaciones2:
        pattern = re.compile(r"(y)")
        matches = re.findall(pattern, item.text)
        nnohabt += len(matches)*2

    if len(infohabitaciones)-1 == 1:
        infohabitaciones = driver.find_element(By.XPATH, '//*[@id="maxotelRoomArea"]/section/div[2]/div[1]/div[2]').text
        #print(infohabitaciones)
        pattern = re.compile(r"(Dormitorio)")
        matches = re.findall(pattern, infohabitaciones)
        #print(len(matches))
        Habitaciones = {"Habitaciones": len(matches)}
    elif len(driver.find_elements(By.XPATH, '//*[@id="maxotelRoomArea"]/section/div/div[1]/div[2]/div'))-nnohabt == len(infohabitaciones)-1:
        Habitaciones = {"Habitaciones": str(len(infohabitaciones)-1)+"+"}
    else:
        pattern = re.compile(r"(Dormitorio)")
        nhabt = 0
        for item in driver.find_elements(By.XPATH, '//*[@id="maxotelRoomArea"]/section/div/div[1]/div[2]'):
            #print("space")
            #print(item.text)
            matches = re.findall(pattern, item.text)
            if len(matches) == 0: nhabt += 1
            else: nhabt += len(matches)
            #print(matches)
            #print(nhabt)
        Habitaciones = {"Habitaciones": str(nhabt)+"+"}

    Camas = {"Camas": bed_count}
    Capacidad = {"Capacidad": bed_count}

    if "+" in str(Habitaciones["Habitaciones"]):
        Camas = {"Camas": str(bed_count)+"+"}
        Capacidad = {"Capacidad": str(bed_count)+"+"}

    #print(Camas)
    #print(Capacidad)
    #print(Habitaciones)
    
    #Precio = {"Precio":driver.find_element(By.XPATH, '//*[@id="site-content"]/div/div[1]/div[3]/div/div[2]/div/div/div[1]/div/div/div/div/div/div/div[1]/div[1]/div[1]/div/span/div/span[1]').text}
    
    try: Nota = {"Nota":driver.find_element(By.XPATH, '//*[@id="guest-featured_reviews__horizontal-block"]/div[2]/div[1]/div/div[2]/div/button/div/div/div[1]').text.replace(",",".")}
    except: Nota = {"Nota": None}
    #print(Nota)
    #try: Nnota = {"Nnota":driver.find_element(By.XPATH, '//*[@id="site-content"]/div/div[1]/div[3]/div/div[2]/div/div/div[1]/div/div/div/div/div/div/div[1]/div[1]/div[2]/span/span[3]/button/span').text}
    #except: Nnota = {"Nota": None}
    
    Descripción = {"Descripción":driver.find_element(By.XPATH, '//*[@id="property_description_content"]').text}
    #print(Descripción)

    Titulo1 = {"Titulo1":driver.find_element(By.XPATH, '//*[@id="hp_hotel_name"]/div/div/h2').text}
    #print(Titulo1)
    
    #Titulo2 = {"Titulo2":driver.find_element(By.XPATH, '//*[@id="site-content"]/div/div[1]/div[3]/div/div[1]/div/div[1]/div/div/section/div/div/div/div[1]/div/h2').text}
    
    Servicios = {"Servicios":driver.find_element(By.XPATH, '//*[@id="hp_facilities_box"]').text}
    #print(Servicios)
    
    try: Anfitrion = {"Anfitrion":driver.find_element(By.XPATH, '//div[@data-testid="host-image"]/../div[2]').text}
    except: Anfitrion = {"Anfitrion": None}
    try: Descripcionanfi = {"Descripcionanfi":driver.find_element(By.XPATH, '//div[@data-testid="host-image"]/../../div[2]').text}
    except: Descripcionanfi = {"Descripcionanfi": None}




    try: text = driver.find_element(By.XPATH, '//p[@class="summary  hotel_meta_style"]').text
    except: text = driver.find_element(By.XPATH, '//p[@class="summary hotel_meta_style"]').text
    #print(text)
    pattern = re.compile(r"(\d+) (\w+) (\d+)")
    # Find all matches in the text:
    matches = re.findall(pattern, text)
    #print(matches)
    if matches:
        try:   
            match = matches[0]
            day, month_str, year = match
            months = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]
            # Convert the month from string to number:
            month = months.index(month_str.lower()) + 1
            # Format the date as desired:
            date = f"{day}/{month}/{year}"
        except: 
            match = matches[1]
            day, month_str, year = match
            months = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]
            # Convert the month from string to number:
            month = months.index(month_str.lower()) + 1
            # Format the date as desired:
            date = f"{day}/{month}/{year}"
    
    Registro = {"Registro":date}
    #print(Registro)
    
    #try: Ubides = {"Ubides":driver.find_element(By.XPATH, '//*[@id="site-content"]/div/div[1]/div[5]/div/div/div/div[2]/div/section/div[4]/div/div/div/div[2]/span/span').text}
    #except: Ubides = {"Ubides":None}
    ubicc = driver.find_element(By.XPATH, '//a[@id="hotel_sidebar_static_map"]').get_attribute("data-atlas-latlng")
    Ubicacion = {"Ubicacion": ubicc}
    #print(Ubicacion)
    lat = {"lat": ubicc.split(",")[0]}
    #print(lat)
    long = {"long": ubicc.split(",")[1]}
    #print(long)
    dicts = [Link, Direccion, Camas, Capacidad, Habitaciones, Nota,
        Descripción, Titulo1, Servicios, Anfitrion, Descripcionanfi, Registro, Ubicacion, lat, long, info_habitaciones]
    #print(dicts)
    for dic in dicts:
        Comuna.update(dic)

    dfmin = pd.DataFrame([Comuna])
    dfpage = pd.concat([dfpage,dfmin])
    df = pd.concat([df,dfmin])
    return df, dfpage

def scrap_links(driver, df, folderpath, pag):
    initial_url = driver.current_url
    #print(type(initial_url))
    #print(initial_url)
    time.sleep(3)
    items = driver.find_elements(By.XPATH, '//a[@data-testid="title-link"]')
    print(len(items), f" Items encontrados en pag {pag}")
    links = []
    dfpage = pd.DataFrame()
    time.sleep(3)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_all_elements_located((By.XPATH, '//a[@data-testid="title-link"]')))

    for item in items:
        #print(item.get_attribute("href"))
        links.append(item.get_attribute("href"))

    for link in links:
        try: df, dfpage = scrap(driver, link, df, folderpath, pag, dfpage)
        except: 
            print("POP UP ACTIVO")
            time.sleep(10)
            #cerrar_button = driver.find_element(By.XPATH, "//button[@aria-label='Cerrar']")
            #cerrar_button.click()
            #time.sleep(3)
            df, dfpage = scrap(driver, link, df, folderpath, pag, dfpage)

    dfpage.to_csv(os.path.join(folderpath,f"Data_{pag}"))
    driver.get(initial_url)

    return df

def siguiente_pagina(driver, pag):
    button = driver.find_element(By.XPATH, '//button[@aria-label="Página siguiente"]')
    print("Cargando siguiente página")
    wait = WebDriverWait(driver, 5)
    clickable = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Página siguiente"]')))
    #linkbut = button.get_attribute("href")
    #print("Link CARGANDO", button.get_attribute("href"))
    if button == clickable:
        button.click()
        y = 0
        pag = pag + 1
        return y, pag
    else: 
        print("NO HAY SIGUIENTE PÁGINA")
        y = 1
        return y, pag

"""
FLUJO DE TRABAJO
"""


driver = opendriver(options)
df = pd.DataFrame()
y = 0
iter = 7
pag = 1

folderpath, dir_path = create_folders(iter)
apertura_marketplace(driver)

while y == 0:
    df = scrap_links(driver, df, folderpath, pag)
    y, pag = siguiente_pagina(driver, pag)

df.to_csv(os.path.join(dir_path,"Data_{iter}"))


