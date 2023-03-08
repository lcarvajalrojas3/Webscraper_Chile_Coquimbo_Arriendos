* Webscraper of the 6 most used property rental pages in Chile:

Specifically oriented to collect data on rentals in the Coquimbo Region, used during February 2023.
Developed for the BIG DATA Research Center of the University of La Serena.
Made centrally with the python Selenium library, in conjunction with others.

* Webscraper der 6 meistgenutzten Immobilienvermietungsseiten in Chile:

Speziell ausgerichtet auf die Erhebung von Daten zu Vermietungen in der Region Coquimbo, verwendet im Februar 2023.
Entwickelt für das BIG DATA Research Center der Universität La Serena.
Zentral erstellt mit der Python-Selenium-Bibliothek, in Verbindung mit anderen.

* Webscraper de las 6 páginas de arriendo de propiedades más usadas en Chile: 

- Yapo
- Airbnb
- Booking
- Trovit
- Marketplace (Facebook)
- Parairnos

Orientado especificamente a recolectar datos sobre arriendos en la Región de Coquimbo, usados durante Febrero 2023. 

Desarrollado para el Centro de investigación de BIG DATA de la Universidad de La Serena, Chile.
Developed for the BIG DATA Research Center of the University of La Serena, Chile.
Entwickelt für das BIG DATA Research Center der Universität La Serena, Chile.

Developed by Luciano Carvajal

-----------------------------------------------------------------------------------------------------
Libraries used

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options ### CONFIGURADO CON EDGE
from datetime import datetime, timedelta
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.proxy import Proxy, ProxyType
import pandas as pd
import numpy as np
import cv2
import pytesseract
import base64
import os
import random
import re
import time









