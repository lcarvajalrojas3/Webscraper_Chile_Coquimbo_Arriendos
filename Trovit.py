from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.edge.options import Options ### CONFIGURADO CON EDGE
import pandas as pd
from datetime import datetime, timedelta
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.proxy import Proxy, ProxyType
#import cv2
#import pytesseract
import base64
import numpy as np
import os
import random
import re

import selenium

"""
FUNCIONES DESARROLLADAS
TEMA - FUNCIÓN

GENERACIÓN DE CARPETAS
    f(x) def create_folder(iter) >>> Genera una carpeta donde guardar los df por página, para la iteración específica.

APERTURA INICIAL
    f(x) def opendriver(options) >>> Abre y define el driver para su ejecución
    f(x) def apertura_portal(driver, busqueda, url) >>> Abre la primera página de resultados de una búsqueda. Se debe proveer la url de esta página inicial,
                                                        no realiza la búsqueda en sí.

CARGA DE LINKS Y SCRAP DE INFO
    f(x) def scrap_links(driver, df, pag) >>> Desde la página de resultados de búsqueda, extrae links de cada aviso, carga cada uno de esos link, y scrapea dependiendo de
                                              la página que se haya abierto, para una vez scrapeados todos los avisos, volver a la página de resultados de búsqueda.
        SUBFUNCIONES - INFOSCRAP:                                      
        f(x) def scrap_trovit(driver, link, df, dfpage) >>> Scrapea info de página de aviso ya cargada, en subportal trovit.
        f(x) def scrap_toctoc(driver, link, df, dfpage) >>> Scrapea info de página de aviso ya cargada, en subportal toctoc.
        f(x) def scrap_tixuz(driver, link, df, dfpage) >>> Scrapea info de página de aviso ya cargada, en subportal tixuz.

CARGA DE SIGUIENTE PÁGINA
    f(x) def siguiente_pagina(driver) >>> Desde la página de resultados de búsqueda, carga la siguiente página. En caso de no haber siguiente página, termina

"""


def create_folders(iter):
    print("\n\nRevisando existencia de carpetas necesarias")
    dir_path = os.path.dirname(os.path.realpath("__file__"))
    print("path local: ", dir_path)
    folderpath = "Trovit"
    folderpath = os.path.join(dir_path, folderpath)
    if not os.path.exists(folderpath):
        os.mkdir(folderpath)
        print("Carpeta Parairnos creada")
    else: print("Carpeta Parairnos existente")
    dir_path = folderpath
    folderpath = f"Data_porpag_{iter}"
    folderpath = os.path.join(dir_path, folderpath)
    if not os.path.exists(folderpath):
        os.mkdir(folderpath)
        print("Subcarpeta Data creada\n\n")
    else: print("Subcarpeta Data Existente")
    return folderpath, dir_path

options = Options()
#prox = Proxy()

#prox.proxy_type = ProxyType.MANUAL
#prox.http_proxy = "75.89.101.60:80"
#prox.socks_proxy = "75.89.101.60:80"
#prox.ssl_proxy = "75.89.101.60:80"

#capabilities = webdriver.DesiredCapabilities.CHROME
#prox.add_to_capabilities(capabilities)

options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument("--disable-notifications")
PROXY = "190.61.88.147:8080"  
options.add_argument('--proxy-server=%s' % PROXY)
options.add_argument("--disable-blink-features=AutomationControlled")

def opendriver(options):
    driver = webdriver.Edge(options=options)#, capabilities=capabilities)
    time.sleep(2)
    driver.maximize_window()
    print("Abriendo WebDriver")
    time.sleep(2)
    return driver

def apertura_portal(driver, busqueda, url):
    driver.get(url)
    time.sleep(3)
    print("Cargando Página y realizando búsqueda de '", busqueda, "'")
    #buscador = driver.find_element(By.XPATH,'//*[@id="parairnosSearch"]')
    #buscador.click()
    #buscador.send_keys(Keys.CONTROL, "a")
    #buscador.send_keys(Keys.DELETE)
    time.sleep(1)
    
    #buscador = driver.find_el ement(By.XPATH, '//input[@id="bigsearch-query-location-input"]')
    #buscador.clear()   ]
    
    #buscador.send_keys(busqueda)
    #button = driver.find_elements(By.XPATH,'//button[@type="submit"]')
    #button[1].click()
    time.sleep(3)

def scrap_links(driver, df, pag):
    initial_url = driver.current_url
    items = driver.find_elements(By.XPATH, '//*[@id="wrapper_listing"]/li/div/div/div[2]/a')
    print(len(items), f"ITEMS ENCONTRADOS EN PAG {pag}")
    links = []
    dfpage = pd.DataFrame()
    for item in items:
        links.append(item.get_attribute("href"))

    for index, link in enumerate(links):
        print("debug1")
        driver.get(link)
        print("debug2")
        time.sleep(random.randint(10, 35))
        print("debug3")

        stringurl = driver.current_url
        print("cargando...", index+1)
        if "tixuz" in stringurl[:25]:
            print("tixuz")
            df, dfpage = scrap_tixuz(driver, link, df, dfpage)
        elif "toctoc" in stringurl[:25]:
            print("toctoc")
            df, dfpage = scrap_toctoc(driver, link, df, dfpage)
        elif "trovit" in stringurl[:25]:
            print("trovit")
            df, dfpage = scrap_trovit(driver, link, df, dfpage)
        else: print("NO CARGA/NO SE RECONOCE")

    driver.get(initial_url)
    dfpage.to_csv(os.path.join(folderpath, f"Data_{pag}"))
    pag = pag + 1
    return df, pag

def scrap_trovit(driver, link, df, dfpage):
    time.sleep(4)
    try:
        try:
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="map"]')))
        except (TimeoutException, NoSuchElementException):
            print("Timed out waiting for element")
        try:
            googlemap = driver.find_element(By.XPATH, '//*[@id="map"]')
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'instant', block: 'center'});", googlemap)
        except (TimeoutException, NoSuchElementException):
            print("Timed out waiting for element")
        link = driver.current_url

        Link = {"Link":link}
        print(Link)
        info_comuna = driver.find_element(By.XPATH, '//*[@id="main_info"]/*[@class="address"]').text
        comuna = info_comuna.split(", ")

        if len(comuna) > 3:
            Comuna = {"Comuna": comuna[1]}
        else:   
            Comuna = {"Comuna": comuna[0]}
        print(Comuna)

        Region = {"Region": comuna[-1]}
        print(Region)

        try: Baños = {"Baños": ''.join(filter(str.isdigit, driver.find_element(By.XPATH, '//div[contains(text(), "Baño")]/span[1]').text))}
        except: Baños = {"Baños": None}
        print(Baños)
        
        try: Habitaciones = {"Habitaciones": ''.join(filter(str.isdigit, driver.find_element(By.XPATH, '//div[contains(text(), "Dorm")]').text))}
        except: Habitaciones = {"Habitaciones": None}
        print(Habitaciones)
        
        try:
            infoprecio = ''.join(filter(str.isdigit, driver.find_element(By.XPATH, '//div[@class="price"]//*[@class="amount"]').text))
            if infoprecio == "":    
                {"Precio": None} 
            else: Precio = {"Precio": infoprecio}
        except: Precio = {"Precio": None}
        print(Precio)

        if "$" in driver.find_element(By.XPATH, '//div[@class="price"]//*[@class="amount"]').text:
            Tipo_precio = {"Tipo_precio": "CLP"}
        elif "UF" in driver.find_element(By.XPATH, '//div[@class="price"]//*[@class="amount"]').text:
            Tipo_precio = {"Tipo_precio": "UF"}
        else: Tipo_precio = {"Tipo_precio": None}
        print(Tipo_precio)

        try: Descripcion = {"Descripción":driver.find_element(By.XPATH, '//*[@id="description"]/p').text.replace("\n", " ")}
        except: Descripcion = {"Descripción":None}
        print(Descripcion)

        try: Titulo1 = {"Titulo1":driver.find_element(By.XPATH, '//*[@id="main_info"]/h1').text}
        except: Titulo1 = {"Titulo1":driver.find_element(By.XPATH, '//*[@class="ap_traffic"]/h1').text}
        print(Titulo1)
        
        try:
            info_servicios = driver.find_elements(By.XPATH, '//*[@id="property_facilities"]/ul/li')
            servicios = []
            for item in info_servicios:
                servicios.append(item.text)
        
            if servicios == []:
                Servicios = {"Servicios": None}
            else: Servicios = {"Servicios": servicios}
        except: Servicios = {"Servicios": None}
        print(Servicios)

        try:
            info_servicios = driver.find_elements(By.XPATH, '//*[@id="building_facilities"]/ul/li')
            servicios = []
            for item in info_servicios:
                servicios.append(item.text)
            
            if servicios == []:
                Servicios_prop = {"Servicios_prop": None}
            else: Servicios_prop = {"Servicios_prop": servicios}
        except: Servicios_prop = {"Servicios_prop": None}
        print(Servicios_prop)

        try:
            Anfitrion = {"Anfitrion": driver.find_elements(By.XPATH, '//div[@class="contact-form-agency-info"]/*/p[@class="agency-name"]')[1].text}
        except: Anfitrion = {"Anfitrion": None}
        print(Anfitrion)

        try: Telefono = {"Telefono": driver.find_element(By.XPATH, '//*[@id="contact-form"]/div[2]/div[1]/div[@class="contact-form-chat-buttons"]/ul/li').get_attribute("data-contact")}
        except: Telefono = {"Telefono": None}
        print(Telefono)

        try: 
            info_direccion = driver.find_element(By.XPATH, '//*[@id="map_section_container"]/div[1]/p').text.split("\n")
            if len(info_direccion) > 1:
                Direccion = {"Direccion": info_direccion[0].split(",")[0]}
            else: Direccion = {"Direccion": None}
        except: Direccion = {"Direccion": None}
        print(Direccion)

        try:
            info_ubicacion = driver.find_element(By.XPATH, '//*[@id="map"]')
            lat = {"long": info_ubicacion.get_attribute("data-latitude")}
            long =  {"long": info_ubicacion.get_attribute("data-longitude")}
        except: 
            lat = {"long": None}
            long =  {"long": None}
        print(lat, long)
        
        try: Superficie = {"Superficie":driver.find_element(By.XPATH, '//div[contains(text(), "Superficie")]/../div[@class="amenity-value"]').text}
        except: Superficie = {"Superficie": None}

        try: Superficie_terreno = {"Superficie_terreno":driver.find_element(By.XPATH, '//div[contains(text(), "Superficie del terreno")]/../div[@class="amenity-value"]').text}
        except: Superficie_terreno = {"Superficie_terreno": None}

        Tipo = {"Tipo":driver.find_element(By.XPATH, '//div[contains(text(), "Tipo de propiedad")]/../div[@class="amenity-value"]').text}
        
        Tipo_anuncio = {"Tipo_anuncio":driver.find_element(By.XPATH, '//div[contains(text(), "Tipo de anuncio")]/../div[@class="amenity-value"]').text}

        try: Amueblado = {"Amueblado":driver.find_element(By.XPATH, '//div[contains(text(), "Amueblado")]/../div[@class="amenity-value"]').text}
        except: Amueblado = {"Amueblado":None}
        print(Amueblado)

        try: Piso = {"Piso":driver.find_element(By.XPATH, '//div[contains(text(), "Piso")]/../div[@class="amenity-value"]').text}
        except: Piso = {"Piso": None}

        try: Año_construccion = {"Año_construccion":driver.find_element(By.XPATH, '//div[contains(text(), "Año de construcción")]/../div[@class="amenity-value"]').text}
        except: Año_construccion = {"Año_construcion": None}

        ScrapDate = {"ScrapDate": datetime.now().date().strftime("%d-%m-%Y")}

        Fuente = {"Fuente": "Trovit"}
        
        dicts = [Link, Region, Baños, Habitaciones, Precio, Tipo_precio, Superficie, Superficie_terreno, Tipo, Tipo_anuncio, Amueblado,
            Descripcion, Titulo1, Servicios, Servicios_prop, Anfitrion, Telefono, lat, long, Piso, Año_construccion, ScrapDate, Fuente]
        
        for dic in dicts:
            Comuna.update(dic)

        dfmin = pd.DataFrame([Comuna])
        dfpage = pd.concat([dfpage, dfmin])

        df = pd.concat([df,dfmin])
        return df, dfpage
    except: 
        print("LINK PERDIDO")
        return df, dfpage

def scrap_toctoc(driver, link, df, dfpage):
    print(link)
    time.sleep(3)
    try:
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="mapFichaUbicacion"]')))
        googlemap = driver.find_element(By.XPATH, '//*[@id="mapFichaUbicacion"]')
        time.sleep(1)
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'instant', block: 'center'});", googlemap)
        
        link = driver.current_url

        Link = {"Link":link}
        print(Link)

        info_comuna = driver.find_element(By.XPATH, '//*[@id="partialCabecera"]/div[1]/header/div/h2')
        comuna = info_comuna.text.replace(" Ver ubicación","").split(" ")
        Comuna = {"Comuna": comuna[-3]}
        print(Comuna)

        Region = {"Region": comuna[-1]}
        print(Region)

        Baños = {"Baños": driver.find_element(By.XPATH, '//ul[@class="info_ficha"]/li[@class="baños"]/strong').text}
        print(Baños)
        
        Habitaciones = {"Habitaciones": ''.join(filter(str.isdigit, driver.find_element(By.XPATH, '//li[@class="dormitorios"]/strong').text))}
        print(Habitaciones)

        infoprecio = ''.join(filter(str.isdigit, driver.find_element(By.XPATH, '//*[@id="partialCabecera"]/div[1]/div/div/div/strong').text))
        if infoprecio == "":    
            infoprecio = None
        else: Precio = {"Precio": infoprecio}
        print(Precio)

        if "$" in driver.find_element(By.XPATH, '//*[@id="partialCabecera"]/div[1]/div/div/div/strong').text:
            Tipo_precio = {"Tipo_precio": "CLP"}
        elif "UF" in driver.find_element(By.XPATH, '//*[@id="partialCabecera"]/div[1]/div/div/div/strong').text:
            Tipo_precio = {"Tipo_precio": "UF"}
        else: Tipo_precio = None
        print(Tipo_precio)

        try: Descripcion = {"Descripción":driver.find_element(By.XPATH, '//*[@id="partialInformacionAdicional"]/div[1]/div[2]').text.replace("\n", " ")}
        except: Descripcion = {"Descripción":None}
        print(Descripcion)

        Titulo1 = {"Titulo1":driver.find_element(By.XPATH, '//*[@id="partialCabecera"]/div[1]/header/h1').text}
        print(Titulo1)
        
        anfi_button = driver.find_element(By.XPATH, '//*[@id="btnVerDatosContacto"]')
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'instant', block: 'center'});", anfi_button)
        anfi_button.click()
        time.sleep(1)
        Anfitrion = {"Anfitrion": driver.find_element(By.XPATH, '//*[@id="partialInformacionContacto"]/div/div[2]/ul/li[3]/div/h5/strong').text}
        print(Anfitrion)

        try: Telefono = {"Telefono": ''.join(filter(str.isdigit, driver.find_element(By.XPATH, '//*[@id="partialInformacionContacto"]/div/div[2]/ul/li[3]/div/p[2]').text))}
        except: Telefono = {"Telefono": None}
        print(Telefono)

        lat = {"long": driver.find_element(By.XPATH, '//*[@id="h_br_lat"]').get_attribute("value")}
        long =  {"long": driver.find_element(By.XPATH, '//*[@id="h_br_lon"]').get_attribute("value")}
        print(lat, long)
        
        try: Superficie = {"Superficie":  str(max(map(int, re.findall(r'\d+', driver.find_element(By.XPATH, '//*[@id="partialCabecera"]/div[1]/header/ul/li[1]').text))))}
        except: Superficie = {"Superficie": None}
        print(Superficie)

        try: Superficie_construida = {"Superficie_construida":''.join(filter(lambda x: x.isdigit() and x != '²', driver.find_element(By.XPATH, '//ul[@class="info_ficha"]/li[@class="metrosConstruidos"]/strong').text))}
        except: Superficie_construida = {"Superficie_construida": None}
        try: Superficie_util = {"Superficie_util":''.join(filter(lambda x: x.isdigit() and x != '²', driver.find_element(By.XPATH, '//ul[@class="info_ficha"]/li[@class="metrosUtiles"]/strong').text))}
        except: Superficie_util = {"Superficie_util": None}
        try: Superficie_terreno = {"Superficie_terreno":''.join(filter(lambda x: x.isdigit() and x != '²', driver.find_element(By.XPATH, '//ul[@class="info_ficha"]/li[@class="metrosTerreno"]/strong').text))}
        except: Superficie_terreno = {"Superficie_terreno": None}
        print(Superficie_construida, Superficie_terreno, Superficie_util)

        info_Tipo = driver.find_element(By.XPATH, '//*[@id="partialCabecera"]/div[1]/header/div/h2').text.split(" ")
        Tipo = {"Tipo": info_Tipo[0]}
        
        if info_Tipo[0] == "Terreno":
            Tipo = {"Tipo": info_Tipo[0]+" "+info_Tipo[1]}
        print(Tipo)

        info_anuncio = driver.find_element(By.XPATH, '//*[@id="partialCabecera"]/div[1]/header/div/h2').text.split(" ")
        Tipo_anuncio = {"Tipo_anuncio":info_anuncio[2]}
        
        if info_anuncio[2] == "en":
            Tipo_anuncio = {"Tipo_anuncio":info_anuncio[3]}
        print(Tipo_anuncio)

        try: Año_construccion = {"Año_construccion": driver.find_element(By.XPATH, '//ul[@class="info_ficha"]/li[@class="año"]/strong').text}
        except: Año_construccion = {"Año_construcion": ""}
        print(Año_construccion)

        Superficie_terraza = {"Superficie_terraza":''.join(filter(lambda x: x.isdigit() and x != '²', driver.find_element(By.XPATH, '//ul[@class="info_ficha"]/li[@class="metrosTerraza"]/strong').text))}
        estacionamientos = {"Estacionamientos":driver.find_element(By.XPATH, '//ul[@class="info_ficha"]/li[@class="estacionamientos"]/strong').text}

        driver.execute_script("arguments[0].scrollIntoView({behavior: 'instant', block: 'center'});", driver.find_element(By.XPATH, '//*[@id="infoEntorno"]'))
        time.sleep(1)
        try:
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'instant', block: 'center'});", driver.find_element(By.XPATH, '//*[@id="headingEntorno"]/h4[contains(text(),"verdes")]'))
            time.sleep(1)
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'instant', block: 'center'});", driver.find_element(By.XPATH, '//*[@id="headingEntorno"]/h4[contains(text(),"Seguridad")]'))

            infoind = driver.find_elements(By.XPATH,'//*[@id="entornoContenidoSeguridad"]/div/div[2]/div[1]/div/span')
            for span in infoind:
                if span.find_elements(By.XPATH, './/small'):
                    ind = span.get_attribute('class')
            ind_delinc = {"Ind_delinc": 6-int(''.join(filter(str.isdigit, ind)))}

            infoind = driver.find_elements(By.XPATH,'//*[@id="entornoContenidoSeguridad"]/div/div[2]/div[2]/div/span')
            for span in infoind:
                if span.find_elements(By.XPATH, './/small'):
                    ind = span.get_attribute('class')
            ind_seguridad = {"Ind_seguridad": ''.join(filter(str.isdigit, ind))}
            
            infoind = driver.find_elements(By.XPATH,'//*[@id="entornoContenidoTransporte"]/div/div[2]/div[2]/div/span')
            for span in infoind:
                if span.find_elements(By.XPATH, './/small'):
                    ind = span.get_attribute('class')
            ind_transporte = {"Ind_transporte": ''.join(filter(str.isdigit, ind))}
        
            Averdexpersona = {"Averdexpersona": ''.join(filter(lambda x: x.isdigit() and x != '²', driver.find_element(By.XPATH, '//*[@id="entornoContenidoAreaVerde"]/div/div[2]/div[2]/p/strong').text))}
            
        except:
            Averdexpersona = {"Averdexpersona": None}
            ind_transporte = {"Ind_transporte": None}
            ind_delinc = {"Ind_delinc": None}
            ind_seguridad = {"Ind_seguridad": None}

        print(ind_delinc)
        print(ind_seguridad)
        print(ind_transporte)
        print(Averdexpersona)
        ScrapDate = {"ScrapDate": datetime.now().date().strftime("%d-%m-%Y")}
        print(ScrapDate)
        Fuente = {"Fuente": "Toctoc"}
        print(Fuente)
        
        dicts = [Link, Titulo1, Region, Baños, Habitaciones, Precio, Tipo_precio, Superficie, Superficie_terreno, Superficie_construida, Superficie_terraza, Tipo, Tipo_anuncio, estacionamientos,
            ind_delinc, ind_seguridad, ind_transporte, Averdexpersona, Descripcion,  Anfitrion, Telefono, lat, long, Año_construccion, ScrapDate, Fuente]
        
        for dic in dicts:
            Comuna.update(dic)

        dfmin = pd.DataFrame([Comuna]).replace("", None)
        dfpage = pd.concat([dfpage, dfmin])

        df = pd.concat([df,dfmin])
        return df, dfpage
    except: 
        print("LINK PERDIDO")
        return df, dfpage

def scrap_tixuz(driver, link, df, dfpage):

    try:
        time.sleep(5)
        print(link)
        print(driver.current_url)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_all_elements_located((By.XPATH, '//p[@itemprop="description"]')))
        googlemap = driver.find_element(By.XPATH, '//p[@itemprop="description"]')
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'instant', block: 'center'});", googlemap)

        link = driver.current_url

        Link = {"Link":link}
        print(Link)

        Region = {"Region": driver.find_element(By.XPATH, '//span[@itemprop="addressRegion"]').text}
        print(Region)

        Baños = {"Baños": ''.join(filter(str.isdigit, driver.find_element(By.XPATH, '//div[@class="composs-main-article-meta"][2]/*[contains(text(), "año")]').text))}
        print(Baños)
        
        Habitaciones = {"Habitaciones": ''.join(filter(str.isdigit, driver.find_element(By.XPATH, '//div[@class="composs-main-article-meta"][2]/*[contains(text(), "camara")]').text))}
        print(Habitaciones)

        infoprecio = ''.join(filter(str.isdigit, driver.find_element(By.XPATH, '//span[@itemprop="price"]').text))
        if infoprecio == "":    
            infoprecio = None
        else: Precio = {"Precio": infoprecio}
        print(Precio)

        if "CLP" in driver.find_element(By.XPATH, '//span[@itemprop="priceCurrency"]').text:
            Tipo_precio = {"Tipo_precio": "CLP"}
        elif "UF" in driver.find_element(By.XPATH, '//span[@itemprop="priceCurrency"]').text:
            Tipo_precio = {"Tipo_precio": "UF"}
        else: Tipo_precio = {"Tipo_precio": None}
        print(Tipo_precio)

        try: Descripcion = {"Descripción":driver.find_element(By.XPATH, '//p[@itemprop="description"]').text.replace("\n", " ")}
        except: Descripcion = {"Descripción":None}
        print(Descripcion)

        Titulo1 = {"Titulo1":driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div/div/div/div/div[1]/div/h1').text}
        print(Titulo1)
        
        try: 
            Superficie = {"Superficie":''.join(filter(lambda x: x.isdigit(),
                driver.find_element(By.XPATH, '//div[@class="composs-main-article-meta"][2]//*[contains(text(), "m2")]/..').text.replace("m2","")))}
        except: Superficie = {"Superficie": None}
        print(Superficie)

        try:
            Estacionamientos = {"Estacionamientos":driver.find_element(By.XPATH, '//div[@class="composs-main-article-meta"][2]//*[contains(text(), "Estacion")]')}
        except: Estacionamientos = {"Estacionamientos":None}

        ScrapDate = {"ScrapDate": datetime.now().date().strftime("%d-%m-%Y")}

        Fuente = {"Fuente": "Tixuz"}
        
        dicts = [Link, Region, Baños, Habitaciones, Precio, Tipo_precio, Superficie, 
            Descripcion, Titulo1, Estacionamientos, ScrapDate, Fuente]
        
        #print(dicts)
        concat = {}
        for dic in dicts:
            concat.update(dic)

        dfmin = pd.DataFrame([concat])
        dfpage = pd.concat([dfpage, dfmin])

        df = pd.concat([df,dfmin])
        return df, dfpage
    except: 
        print("LINK PERDIDO")
        return df, dfpage

def siguiente_pagina(driver):
    try: 
        button = driver.find_element(By.XPATH, '//p[@class="trovit-paginator"]/a[contains(text(),"Siguiente")]')
        print("Cargando siguiente página    ----------------------------------------------------------------------------")
        #time.sleep(5)
        #print("Link CARGANDO", button.get_attribute("href"))
        #if button.is_enabled():
        driver.get(button.get_attribute("href"))
        print("debug  z")
        y = 0
        return y
    except: 
        print("NO HAY SIGUIENTE PÁGINA")
        y = 1
        return y


"""
FLUJO DE TRABAJO
"""

iter = 1
busqueda = "Coquimbo"

df = pd.DataFrame()
pag = 93
y = 0

url = f"https://casas.trovit.cl/index.php/cod.search_homes/type.2/what_d.Coquimbo%20Region/origin.2/rooms_min.0/bathrooms_min.0/region.Coquimbo/order_by.relevance/resultsPerPage.25/isUserSearch.1/page.{pag}"


folderpath, dir_path = create_folders(iter)
driver = opendriver(options)
apertura_portal(driver, busqueda, url)

while y == 0:
    try:
        df, pag = scrap_links(driver, df, pag)
        y = siguiente_pagina(driver)
    except: 
        print("ERROR, ERROR, ERROR, VOLVIENDO A CARGAR PAGINA DE 0", f" desde pag {pag}")
        time.sleep(100)
        driver.get(f"https://casas.trovit.cl/index.php/cod.search_homes/type.2/what_d.Coquimbo%20Region/origin.2/rooms_min.0/bathrooms_min.0/region.Coquimbo/order_by.relevance/resultsPerPage.25/isUserSearch.1/page.{pag}")

df.to_csv(os.path.join(dir_path, f"Data_total{iter}"))