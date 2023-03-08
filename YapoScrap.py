from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.edge.options import Options ### CONFIGURADO CON EDGE
import pandas as pd
from datetime import datetime, timedelta
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#import cv2
#import pytesseract
import base64
import numpy as np
import os

"""
FUNCIONES DESARROLLADAS
TEMA - FUNCIÓN

ENTRADA INICIAL
    f(x): APERTURA DE DRIVER - def opendriver() << CONFIGURADO CON EDGE >> 
    f(x): LOGIN DE CUENTA - def login() ## (Desactivado)
    f(x): CARGA DE PÁGINA INICIAL - def paginainicial()

RECOPILACIÓN DE LINKS/INFO GENERAL
    f(x): SCRAP DE LINKS - def prescrap()

CARGA DE LINK Y RECOPILACIÓN INFO ESPECIFICA
    f(x): INFOSCRAP - infoscrap()
        Preprocesado:
        f(x): String to Dates - def convert_to_date()
        f(x): Imagen-Teléfono - def convert_data_url_to_image() ## Desactivado - requiere login

VUELTA A PAG "INICIAL" Y SELECCIÓN DE PÁGINA SIGUIENTE
        f(x): SIGUIENTE PAGINA - def nextpage() >>>> SALIDA Y TÉRMINO EN CASO DE NO EXISTIR SIGUIENTE PÁGINA

EXPORTACIÓN DE DF TOTAL
    f(x): RECOPILACION DE DFs GENERADOS Y CONCATENACIÓN - guardado_df()

SCRAP DE LINKS PERIDDOS (QUE DIERON ERROR)
    f(x): SCRAP DE LINKSFALLIDOS - failedlinkscrap()

"""

def opendriver():
    driver = webdriver.Edge(options=options)
    time.sleep(2)
    driver.maximize_window()
    print("Abriendo WebDriver")
    time.sleep(2)
    return driver

#def login():
 #   global driver
  #  loginurl = "https://www2.yapo.cl/login"
   # driver.get(loginurl)
#    print("Cargando página de Log-in")
 #   wait = WebDriverWait(driver, 10)
  #  wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*')))
    #time.sleep(3)

#    driver.find_element(By.XPATH,'//*[@id="email_input"]').click()
 #   driver.find_element(By.XPATH,'//*[@id="email_input"]').clear()
  #  driver.find_element(By.XPATH,'//*[@id="email_input"]').send_keys("<<mail de ingreso>>")

   # driver.find_element(By.XPATH,'//*[@id="password_input"]').click()
   # driver.find_element(By.XPATH,'//*[@id="password_input"]').clear()
   # driver.find_element(By.XPATH,'//*[@id="password_input"]').send_keys("<<clave a ingresar>>")

   # driver.find_element(By.XPATH,'//*[@id="submit_button"]').click()
   # time.sleep(1)
   # print("Cuenta Logueada")

def paginainicial(driver, mainurl):
    try:
        driver.get(mainurl)
        print("Cargando página inicial")
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*/listing-result-ad/a')))
        print("Página inicial cargada")
    except:
        time.sleep(3)
        paginainicial(driver, mainurl)

def prescrap(driver):
    print("Preanalizando página")
    try:
        items = driver.find_elements(By.XPATH,'//*/listing-result-ad/a')
        print("items encontrados", len(items))
        print("recopilando links e info de pag principal")
        listoflinks = []
        listofcomunas = []
        listofusers = []
        dfpage = pd.DataFrame(columns=["Link","Comuna","Tipousuario"])
        for item in items:
            comunasx = item.find_element(By.XPATH,'.//div[2]/div/div/div/div/p')
            #print(comunasx.text)
            listofcomunas.append(comunasx.text)
            try: 
                userx = item.find_element(By.XPATH, './/div[2]/div[2]/p')
                #print(userx.text)
                listofusers.append(userx.text)
            except: 
                userx = None
                listofusers.append(userx)
            link = item.get_attribute("href")
            #print(str(link))
            listoflinks.append(link)
        dfpage["Link"] = listoflinks
        dfpage["Comuna"] = listofcomunas
        dfpage["Tipousuario"] = listofusers

        print("links recopilados: ",len(listoflinks),"\n\n")
        return dfpage, listoflinks
    except: 
        print("Falla de prescrap, reiniciando página")
        time.sleep(180)
        paginainicial()
        prescrap(driver)
    



def infoscrap(dfpage, driver, listoflinks, y, linksfallidos):
    print("\n\nIniciando scrapping de página ", y)
    dfproductospag = pd.DataFrame(columns = ["Link", "Direccion", "Habitaciones", "Baños", "Precio", "Descripcion", "Titulo1", "Scrapdate",
                "Anfitrion", "Ubicacion", "Fechapubli", "Avisospublicados", "Tipo", "Estacionamiento", "Avisosactivosfecha"])#, "Telefono"])
    for product in listoflinks:
        try:
            driver.get(product)
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_all_elements_located((By.XPATH, '//adview-publisher/div/div[1]/div[1]/p[1]')))
            time.sleep(5)
            Link = product
            print(Link)
            Direccion = (driver.find_elements(By.XPATH,'//*/adview-price-info/div/div/div[1]/p'))[0].text
            try:
                path = driver.find_element(By.XPATH,'//div[@class="features inmo"]/div/div/p[contains(text(), "Dormitorios ")]')
                Habitaciones = path.find_element(By.XPATH,'..')
                Habitaciones = Habitaciones.find_element(By.XPATH, './/p[2]').text # + path.text}
            except:
                Habitaciones = None
            try:
                path = driver.find_element(By.XPATH,'//div[@class="features inmo"]/div/div/p[contains(text(), "Baños ")]')
                Baños = path.find_element(By.XPATH,'..')
                Baños = Baños.find_element(By.XPATH, './/p[2]').text # + path.text}
            except:
                Baños = None
            try:
                Precio = driver.find_elements(By.XPATH,'//adview-index/div/div[2]/div/div[1]/div[1]/adview-price-info/div/div[1]/p[1]')[0].text
            except: Precio = None
            Descripcion = driver.find_element(By.XPATH, '//adview-description/div/p').text.replace("\n", " ")
            Titulo1 = driver.find_element(By.XPATH, '//adview-price-info/div/h1').text
            Anfitrion = driver.find_element(By.XPATH, '//adview-user-avatar/div/div[2]/p').text
            try: 
                Ubicacion = driver.find_element(By.XPATH, '//adview-map/div').get_attribute("style")
                start = Ubicacion.index("lat=")
                end = Ubicacion.index("&lon=")
                start2 = Ubicacion.index("lon=")
                end2 = Ubicacion.index("&h=")
                Ubicacion = [Ubicacion[start:end], Ubicacion[start2:end2]]
            except: Ubicacion = None
            Fechapubli = convert_to_date(driver.find_element(By.XPATH, '//adview-price-info/div/div/div[2]/p').text)
            Avisospublicados = driver.find_element(By.XPATH,'//adview-publisher/div/div[1]/div[1]/p[1]').text
            path = driver.find_element(By.XPATH,'//div[@class="features inmo"]/div/div/p[contains(text(), "Tipo de inmueble ")]')
            Tipo = path.find_element(By.XPATH,'..')
            Tipo = Tipo.find_element(By.XPATH, './/p[2]').text # + path.text}
            try:
                path = driver.find_element(By.XPATH,'//div[@class="features inmo"]/div/div/p[contains(text(), "Estacionamientos")]')
                Estacionamiento = path.find_element(By.XPATH,'..')
                Estacionamiento = Estacionamiento.find_element(By.XPATH, './/p[2]').text # + path.text}
            except:
                Estacionamiento = None
            Avisosactivosfecha = driver.find_element(By.XPATH,'//adview-publisher/div/div[1]/div[2]/p[1]').text

            #try: #### RECOPILACIÓN DE NÚMERO TELEFÓNICO adosado a f(x) image_to_string()
            #    phonebutton = driver.find_element(By.XPATH,'//adview-phone-button/button')
            #    phonebutton.click()
            #    wait = WebDriverWait(driver, 10)
            #    wait.until(EC.presence_of_all_elements_located((By.XPATH, '//adview-phone-button/div/img[2]')))
            #    phoneimg = driver.find_element(By.XPATH,'//adview-phone-button/div/img[2]')
            #    img_url = phoneimg.get_attribute("src")
            #    image = convert_data_url_to_image(img_url)
            #    trans_mask = image[:,:,3] == 0
                #replace areas of transparency with white and not transparent
            #    image[trans_mask] = [255, 255, 255, 255]
                #new image without alpha channel...
            #    new_img = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)
                # OCR
            #    phonenumber = pytesseract.image_to_string(new_img)
            #    Telefono = {"Telefono": phonenumber}
            #except: 
            #    phonenumber = None
            #    Telefono = {"Telefono": None}

            Scrapdate = datetime.now().date().strftime("%d-%m-%Y")  

            ### DEBUG AREA
            #print(Habitaciones)
            #print(Baños)
            #print(Precio)
            #print(Descripcion)
            #print(Titulo1)
            #print(Anfitrion)
            #print(Link)
            #print(Direccion)
            #print(Ubicacion)
            print(driver.find_element(By.XPATH, '//adview-price-info/div/div/div[2]/p').text)
            print(Fechapubli)
            #try:
            #    print(phonenumber)
            #except: continue
            #print(Avisospublicados)
            #print(Avisosactivosfecha)
            #print(Tipo)
            #print(Estacionamiento)
            #print(Fechascrap)
            #print("\n\n")

            dict = {"Link": Link, "Direccion": Direccion, "Habitaciones": Habitaciones, "Baños": Baños, "Precio": Precio, "Descripcion": Descripcion, 
                    "Titulo1": Titulo1, "Anfitrion": Anfitrion, "Ubicacion": Ubicacion, "Fechapubli": Fechapubli, "Avisospublicados": Avisospublicados, 
                    "Tipo": Tipo, "Estacionamiento": Estacionamiento, "Avisosactivosfecha": Avisosactivosfecha, "Scrapdate": Scrapdate} ##Telefono

            dfproductospag = pd.concat([pd.DataFrame([dict]), dfproductospag])
        except: 
            print("scrap de link perdido\n", product)
            linksfallidos.append(product)
            time.sleep(180)

    try:
        print("Generando df de pagina")
        dfpage = dfpage.merge(dfproductospag, on="Link", suffixes=("", ""))
        for n in range (0,len(dfpage["Direccion"]),1):
            dfpage["Direccion"][n] = dfpage["Direccion"][n].replace(dfpage["Comuna"][n],"")
        if dfpage["Direccion"][n] == "":
            dfpage["Direccion"][n] = None
        dir_path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(dir_path, "Yapo/porpag", f"yapopag{y}.csv")
        dfpage.to_csv(file_path, index=False)
        print("Scrapping de página ", y," listo")
        y += 1
        return dfpage, y
    except: 
        print("\nScrap de pag ", y, " fallido, reiniciando --------------------------------------------------------------\n")
        time.sleep(180)
        infoscrap(dfpage, driver, listoflinks, y, linksfallidos)

def convert_to_date(input_string):
    #print(input_string)
    #print(type(input_string))
    current_date = datetime.now().date()
    if "Hoy" in input_string:
        date = current_date
    elif "Ayer" in input_string:
        date = current_date - timedelta(days=1)
    elif "lunes" in input_string:
        days_diff = (current_date.weekday() - 0 + 7) % 7  # 0 represents Monday
        date = current_date - timedelta(days=days_diff)
    elif "martes" in input_string:
        days_diff = (current_date.weekday() - 1 + 7) % 7  # 1 represents Tuesday
        date = current_date - timedelta(days=days_diff)
    elif "miércoles" in input_string:
        days_diff = (current_date.weekday() - 2 + 7) % 7  # 2 represents Wednesday
        date = current_date - timedelta(days=days_diff)
    elif "jueves" in input_string:
        days_diff = (current_date.weekday() - 3 + 7) % 7  # 3 represents Thursday
        date = current_date - timedelta(days=days_diff)
    elif "viernes" in input_string:
        days_diff = (current_date.weekday() - 4 + 7) % 7  # 4 represents Friday
        date = current_date - timedelta(days=days_diff)
    elif "sábado" in input_string:
        days_diff = (current_date.weekday() - 5 + 7) % 7  # 5 represents Saturday
        date = current_date - timedelta(days=days_diff)
    elif "domingo" in input_string:
        days_diff = (current_date.weekday() - 6 + 7) % 7  # 6 represents Sunday
        date = current_date - timedelta(days=days_diff)
    elif "/" in input_string:
        day, month, year = input_string.split("/")
        day = day.split(" ")
        date = datetime.strptime(f"{day[1]}-{month}-{year}", "%d-%m-%Y").date()
    else:
        day, month, year = input_string.split()[0:3]
        month = month[:3]
        month_dict = {
            "ene": "01",
            "feb": "02",
            "mar": "03",
            "abr": "04",
            "may": "05",
            "jun": "06",
            "jul": "07",
            "ago": "08",
            "sep": "09",
            "oct": "10",
            "nov": "11",
            "dic": "12"
        }
        month = month_dict[month]
        date = f"{day}-{month}-{year}"
    return date.strftime("%d-%m-%Y")


#def convert_data_url_to_image(data_url):
    # Decode the data URL into binary data
 #   image_data = base64.b64decode(data_url.split(',')[1])
    
  #  image = cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_UNCHANGED)
    
    # Return the file path
   # return image



def nextpage(driver, mainurl, finish):
    try:
        driver.get(mainurl)
        wait = WebDriverWait(driver, 10)
        button = wait.until(EC.element_to_be_clickable((By.XPATH,'//div/div/a[contains(@aria-label, "siguiente")]')))
        nexturl = button.get_attribute("href")
        if button.is_enabled():
            button.click()
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*/listing-result-ad/a')))
            mainurl = nexturl
            return mainurl, finish
        else: 
            finish = 1
            print("----------------------- PROCESO DE SCRAPPING FINALIZADO ---------------------")
            return mainurl, finish
    except: 
        finish = 1
        print("----------------------- PROCESO DE SCRAPPING FINALIZADO ---------------------")
        return mainurl, finish

def failedlinkscrap(driver, linksfallidos):
    print("\n\nIniciando scrapping de página ", y)
    dfproductospag = pd.DataFrame(columns = ["Link", "Direccion", "Habitaciones", "Baños", "Precio", "Descripcion", "Titulo1", "Scrapdate",
                "Anfitrion", "Ubicacion", "Fechapubli", "Avisospublicados", "Tipo", "Estacionamiento", "Avisosactivosfecha"])#, "Telefono"])
    for product in linksfallidos:
        try:
            driver.get(product)
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_all_elements_located((By.XPATH, '//adview-publisher/div/div[1]/div[1]/p[1]')))
            #time.sleep(3)
            Link = product
            print(Link)
            Direccion = (driver.find_elements(By.XPATH,'//*/adview-price-info/div/div/div[1]/p'))[0].text
            try:
                path = driver.find_element(By.XPATH,'//div[@class="features inmo"]/div/div/p[contains(text(), "Dormitorios ")]')
                Habitaciones = path.find_element(By.XPATH,'..')
                Habitaciones = Habitaciones.find_element(By.XPATH, './/p[2]').text # + path.text}
            except:
                Habitaciones = None
            try:
                path = driver.find_element(By.XPATH,'//div[@class="features inmo"]/div/div/p[contains(text(), "Baños ")]')
                Baños = path.find_element(By.XPATH,'..')
                Baños = Baños.find_element(By.XPATH, './/p[2]').text # + path.text}
            except:
                Baños = None
            try:
                Precio = driver.find_elements(By.XPATH,'//adview-index/div/div[2]/div/div[1]/div[1]/adview-price-info/div/div[1]/p[1]')[0].text
            except: Precio = None
            Descripcion = driver.find_element(By.XPATH, '//adview-description/div/p').text.replace("\n", " ")
            Titulo1 = driver.find_element(By.XPATH, '//adview-price-info/div/h1').text
            Anfitrion = driver.find_element(By.XPATH, '//adview-user-avatar/div/div[2]/p').text
            try: 
                Ubicacion = driver.find_element(By.XPATH, '//adview-map/div').get_attribute("style")
                start = Ubicacion.index("lat=")
                end = Ubicacion.index("&lon=")
                start2 = Ubicacion.index("lon=")
                end2 = Ubicacion.index("&h=")
                Ubicacion = [Ubicacion[start:end], Ubicacion[start2:end2]]
            except: Ubicacion = None
            Fechapubli = convert_to_date(driver.find_element(By.XPATH, '//adview-price-info/div/div/div[2]/p').text)
            Avisospublicados = driver.find_element(By.XPATH,'//adview-publisher/div/div[1]/div[1]/p[1]').text
            path = driver.find_element(By.XPATH,'//div[@class="features inmo"]/div/div/p[contains(text(), "Tipo de inmueble ")]')
            Tipo = path.find_element(By.XPATH,'..')
            Tipo = Tipo.find_element(By.XPATH, './/p[2]').text # + path.text}
            try:
                path = driver.find_element(By.XPATH,'//div[@class="features inmo"]/div/div/p[contains(text(), "Estacionamientos")]')
                Estacionamiento = path.find_element(By.XPATH,'..')
                Estacionamiento = Estacionamiento.find_element(By.XPATH, './/p[2]').text # + path.text}
            except:
                Estacionamiento = None
            Avisosactivosfecha = driver.find_element(By.XPATH,'//adview-publisher/div/div[1]/div[2]/p[1]').text

            #try: #### RECOPILACIÓN DE NÚMERO TELEFÓNICO adosado a f(x) image_to_string()
            #    phonebutton = driver.find_element(By.XPATH,'//adview-phone-button/button')
            #    phonebutton.click()
            #    wait = WebDriverWait(driver, 10)
            #    wait.until(EC.presence_of_all_elements_located((By.XPATH, '//adview-phone-button/div/img[2]')))
            #    phoneimg = driver.find_element(By.XPATH,'//adview-phone-button/div/img[2]')
            #    img_url = phoneimg.get_attribute("src")
            #    image = convert_data_url_to_image(img_url)
            #    trans_mask = image[:,:,3] == 0
                #replace areas of transparency with white and not transparent
            #    image[trans_mask] = [255, 255, 255, 255]
                #new image without alpha channel...
            #    new_img = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)
                # OCR
            #    phonenumber = pytesseract.image_to_string(new_img)
            #    Telefono = {"Telefono": phonenumber}
            #except: 
            #    phonenumber = None
            #    Telefono = {"Telefono": None}

            Scrapdate = datetime.now().date().strftime("%d-%m-%Y")

            ### DEBUG AREA
            #print(Habitaciones)
            #print(Baños)
            #print(Precio)
            #print(Descripcion)
            #print(Titulo1)
            #print(Anfitrion)
            #print(Link)
            #print(Direccion)
            #print(Ubicacion)
            print(driver.find_element(By.XPATH, '//adview-price-info/div/div/div[2]/p').text)
            print(Fechapubli)
            #try:
            #    print(phonenumber)
            #except: continue
            #print(Avisospublicados)
            #print(Avisosactivosfecha)
            #print(Tipo)
            #print(Estacionamiento)
            #print(Fechascrap)
            #print("\n\n")

            dict = {"Link": Link, "Direccion": Direccion, "Habitaciones": Habitaciones, "Baños": Baños, "Precio": Precio, "Descripcion": Descripcion, 
                    "Titulo1": Titulo1, "Anfitrion": Anfitrion, "Ubicacion": Ubicacion, "Fechapubli": Fechapubli, "Avisospublicados": Avisospublicados, 
                    "Tipo": Tipo, "Estacionamiento": Estacionamiento, "Avisosactivosfecha": Avisosactivosfecha, "Scrapdate": Scrapdate} ##Telefono

            dfproductospag = pd.concat([pd.DataFrame([dict]), dfproductospag])
            linksfallidos.remove(product)
        except: 
            print("scrap de link perdido\n", product)
            time.sleep(180)
            failedlinkscrap(driver, linksfallidos)

    dflinksperdidos = dfproductospag
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, "Yapo/porpag", "yapolinksperdidos.csv")
    dflinksperdidos.to_csv(file_path, index=False)
    print("Scrapping de página ", y," listo")
    return dflinksperdidos




def guardado_df():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    folderpath = "Yapo\porpag"
    folderpath = os.path.join(dir_path, folderpath)

    files = []

    for filename in os.listdir(folderpath):
        file_path = os.path.join(folderpath, filename)
        if os.path.isfile(file_path):
            files.append(file_path)


    df = pd.DataFrame(columns=['Link', 'Comuna', 'Tipousuario', 'Direccion', 'Habitaciones', 'Baños', 
        'Precio', 'Descripcion', 'Titulo1', 'Anfitrion', 'Ubicacion',
        'Fechapubli', 'Avisospublicados', 'Tipo', 'Estacionamiento', 'Avisosactivosfecha', 'Scrapdate'])

    for file in files:
        df_file = pd.read_csv(file)
        df = pd.concat([df, df_file])

    print(df.shape)

    dfpath = os.path.join(folderpath, "Df_total.csv")
    df.to_csv(dfpath, index=False)

    print("\n\nDATAFRAME FINAL TOTAL GUARDADO -----------------------------------------------")
    return df


"""
FLUJO DE SCRAPPER

- INICIO -> Definición de variables iniciales
- Apertura de driver
- Carga de página inicial
- Generación de loop (while)
    - Recopilación de links de catálogo
    - Revisión de cada link y guardado de df
    - Vuelta a página main, y selección de próxima pág
        >>> término al no haber más páginas

- Obtención de lista de dfs descargados (uno por página de direcciones)
- Guardado de Df Total
- Obtención de info de links perdidos y guardado

"""

if __name__ == "__main__":

    options = Options()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    linksfallidos = []
    finish = 0
    mainurl = "https://new.yapo.cl/coquimbo/inmuebles/inmuebles/arriendo-temporada"
    #mainurl = "https://new.yapo.cl/coquimbo/inmuebles/inmuebles/arrendar"
    y = 1

    driver = opendriver()
    #login()
    paginainicial(driver, mainurl)

    while finish == 0:
        dfpage, listoflinks = prescrap(driver)
        dfpage, y = infoscrap(dfpage, driver, listoflinks, y, linksfallidos)
        mainurl, finish = nextpage(driver, mainurl, finish)

    df = guardado_df()

    dflinksperdidos = failedlinkscrap(driver, linksfallidos)



