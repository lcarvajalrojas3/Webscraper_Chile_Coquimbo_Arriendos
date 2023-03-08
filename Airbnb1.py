from requests_html import HTMLSession
import pandas as pd
import time

""" AIRBNB ---------------------------------------------------------------------------------------  """ 
r"""

for z in range(1,16,1): 
	try:
		print(f"\n\n\nINICIANDO PRUEBA LA SERENA {z} --------------------------------------------------- \n\n")
		#print(f"C:/Users/bigdatauls/Documents/workspace/python/Webscrapper_arriendos/AirbnbLaSerenapruebacheeckpoint{z}.csv")
		#print(f"C:/Users/bigdatauls/Documents/workspace/python/Webscrapper_arriendos/AirbnbLaSerenaprueba{z}.csv")
		#print(f"C:/Users/bigdatauls/Documents/workspace/python/Webscrapper_arriendos/AirbnbLaSerenapruebakillerror{z}.csv")

		url = "https://www.airbnb.cl/s/La-Serena--Chile/homes?adults=1"
		s = HTMLSession()
		r = s.get(url)
		print("Rendering initial url ---------------------------- INITIALIZING")
		r.html.render(scrolldown=8, sleep=3)

		print("Status:", r.status_code)

		items = r.html.xpath('//*[@id="site-content"]/div[2]/div[2]/div/div/div/div/div', first=True)

		print("links found: ", len(list(items.absolute_links)))

		df = pd.DataFrame(columns=["Link", "Comuna", "Camas", "Baños", "Capacidad", "Habitaciones", "Precio", "Nota", "Nnota",
							"Descripción", "Titulo1", "Titulo2", "Servicios", "Anfitrion", "Registro", "Ubides", "Ubicacion", "Tipo"])
		count = 0
		try:
			for n in range(0,15,1):
				try:
					print("scrapping info page ", n+1)
					for link in items.absolute_links:
						try:
							print(link)
							r = s.get(link)
							r.html.render(scrolldown=15, sleep=2)
							#print(type(r.html.render(scrolldown=1, sleep=5)))
							#with open(r"C:\Users\Luciano Carvajal\Documents\ESTUDIOS\UFRO\ULS\Webscrapper arriendos\file.html", 
							#            "w", encoding='utf-8') as file:
							#    file.write(r.html.html)
							Link = {"Link":link}
							Comuna = {"Comuna": r.html.xpath('//*[@id="site-content"]/div/div[1]/div[1]/div[1]/div/div/div/div/section/div[2]/div[1]/span/button/span/text()')}
							Camas = {"Camas": r.html.xpath('//*[@id="site-content"]/div/div[1]/div[3]/div/div[1]/div/div[1]/div/div/section/div/div/div/div[1]/ol/li[3]/span[2]/text()')}
							Baños = {"Baños":r.html.xpath('//*[@id="site-content"]/div/div[1]/div[3]/div/div[1]/div/div[1]/div/div/section/div/div/div/div[1]/ol/li[4]/span[2]/text()')}
							Capacidad = {"Capacidad":r.html.xpath('//*[@id="site-content"]/div/div[1]/div[3]/div/div[1]/div/div[1]/div/div/section/div/div/div/div[1]/ol/li[1]/span[1]/text()')}
							Habitaciones = {"Habitaciones":r.html.xpath('//*[@id="site-content"]/div/div[1]/div[3]/div/div[1]/div/div[1]/div/div/section/div/div/div/div[1]/ol/li[2]/span[2]/text()')}
							Precio = {"Precio":r.html.xpath('//*[@id="site-content"]/div/div[1]/div[3]/div/div[2]/div/div/div[1]/div/div/div/div/div/div/div[1]/div[1]/div[1]/div/span/div/span[1]/text()')}
							Nota = {"Nota":r.html.xpath('//*[@id="site-content"]/div/div[1]/div[3]/div/div[2]/div/div/div[1]/div/div/div/div/div/div/div[1]/div[1]/div[2]/span/span[2]/text()')}
							Nnota = {"Nnota":r.html.xpath('//*[@id="site-content"]/div/div[1]/div[3]/div/div[2]/div/div/div[1]/div/div/div/div/div/div/div[1]/div[1]/div[2]/span/span[3]/button/span/text()')}
							Descripción = {"Descripción":r.html.xpath('//*[@data-section-id="DESCRIPTION_DEFAULT"]/div/div/span/span/text()')}
							Titulo1 = {"Titulo1":r.html.xpath('//*[@id="site-content"]/div/div[1]/div[1]/div[1]/div/div/div/div/section/div[1]/span/h1/text()')}
							Titulo2 = {"Titulo2":r.html.xpath('//*[@id="site-content"]/div/div[1]/div[3]/div/div[1]/div/div[1]/div/div/section/div/div/div/div[1]/div/h2/text()')}
							Servicios = {"Servicios":r.html.xpath('//*[@data-section-id="AMENITIES_DEFAULT"]/section/div[3]/div')}
							Anfitrion = {"Anfitrion":r.html.xpath('//*[@id="site-content"]/div/div[1]/div[6]/div/div/div/div[2]/div/section/div[1]/div[2]/h2/text()')}
							Registro = {"Registro":r.html.xpath('//*[@id="site-content"]/div/div[1]/div[6]/div/div/div/div[2]/div/section/div[1]/div[2]/div/ol/li/text()')}
							Ubides = {"Ubides":r.html.xpath('//*[@id="site-content"]/div/div[1]/div[5]/div/div/div/div[2]/div/section/div[4]/div/div/div/div[2]/span/span/text()')}
							Ubicacion = {"Ubicacion":r.html.xpath('//*[@class="gm-style"]/div/div/a/@href')}
							dicts = [Link, Camas, Baños, Capacidad, Habitaciones, Precio, Nota, Nnota,
									Descripción, Titulo1, Titulo2, Servicios, Anfitrion, Registro, Ubides, Ubicacion]
							for dic in dicts:
								Comuna.update(dic)

							dfmin = pd.DataFrame([Comuna])
							df = pd.concat([df, dfmin], ignore_index=True)
						except:
							print("ERROR ON PAGE ", n+1, "\n LINK ", link, "\n CONTINUING SCRAPPING                                     ****   ****   ****")
							time.sleep(60)
										
						
					count += 1
					print("pag", count, " lista")
					if count == 15:
						break
					
					print("rendering again page ", count)
					r = s.get(url)
					r.html.render(scrolldown=8, sleep=4)
					print("Status:", r.status_code)
					button = r.html.xpath('//*[@aria-label="Siguiente"]/@href', first=True)
					print("next button found")
					next_url = "https://www.airbnb.cl" + button
					#print(next_url)
					r = s.get(next_url)
					url = next_url
					print("rendering next page \n\n\n\nRendering page ", count+1, " ---------------------------------------")
					print(url)
					r.html.render(scrolldown=8, sleep=4)
					print("Status: ", r.status_code)

					items = r.html.xpath('//*[@id="site-content"]/div[2]/div[2]/div/div/div/div/div', first=True)
					print("links found: ", len(list(items.absolute_links)))
					
				except: 
					print("ERROR EN PAG ", count+1)
					print(f"C:/Users/bigdatauls/Documents/workspace/python/Webscrapper_arriendos/AirbnbLaSerenapruebacheeckpoint{z}.csv")
					df.to_csv(f"C:/Users/bigdatauls/Documents/workspace/python/Webscrapper_arriendos/AirbnbLaSerenapruebacheeckpoint{z}.csv")
					print("CHECKPOINT CSV EXPORTED")
					time.sleep(100)
					print("CONTINUING FOR LOOP")
					
					count += 1
					print("pag", count, " saltada")
					if count == 15:
						break
					
					print("rendering again page ", count)
					#print(url)
					r = s.get(url)
					r.html.render(scrolldown=8, sleep=4)
					print("Status:", r.status_code)
					button = r.html.xpath('//*[@aria-label="Siguiente"]/@href', first=True)
					print("next button found")
					next_url = "https://www.airbnb.cl" + button
					#print(next_url)
					r = s.get(next_url)
					url = next_url
					print("rendering next page \n\nRendering page ", count+1, " ---------------------------------------")
					#print(url)
					r.html.render(scrolldown=8, sleep=4)
					print("Status: ", r.status_code)

					items = r.html.xpath('//*[@id="site-content"]/div[2]/div[2]/div/div/div/div/div', first=True)
					print("links found: ", len(list(items.absolute_links)))
				

			df.to_csv(f"C:/Users/bigdatauls/Documents/workspace/python/Webscrapper_arriendos/AirbnbLaSerenaprueba{z}.csv")
			print(f"C:/Users/bigdatauls/Documents/workspace/python/Webscrapper_arriendos/AirbnbLaSerenaprueba{z}.csv")
			print("FINAL CSV EXPORTED")
		except:
			print("MASTER KILLING ERROR ON PAGE ", count+1)
			print(f"C:/Users/bigdatauls/Documents/workspace/python/Webscrapper_arriendos/AirbnbLaSerenapruebakillerror{z}.csv") 
			df.to_csv(f"C:/Users/bigdatauls/Documents/workspace/python/Webscrapper_arriendos/AirbnbLaSerenapruebakillerror{z}.csv")
			print("KILL ERROR CSV EXPORTED")
			time.sleep(60)
	except: 
		print("\n\n\nERROR DE ITERACIÓN, CONTINUANDO FOR LOOP\n\n\n")
		time.sleep(60)
"""



r"""


for z in range(1,16,1): 
	try:
		print(f"\n\n\nINICIANDO PRUEBA COQUIMBO {z} --------------------------------------------------- \n\n")
		#print(f"C:/Users/bigdatauls/Documents/workspace/python/Webscrapper_arriendos/AirbnbLaSerenapruebacheeckpoint{z}.csv")
		#print(f"C:/Users/bigdatauls/Documents/workspace/python/Webscrapper_arriendos/AirbnbLaSerenaprueba{z}.csv")
		#print(f"C:/Users/bigdatauls/Documents/workspace/python/Webscrapper_arriendos/AirbnbLaSerenapruebakillerror{z}.csv")

		url = "https://www.airbnb.cl/s/Coquimbo--Chile/homes?adults=1"
		s = HTMLSession()
		r = s.get(url)
		print("Rendering initial url ---------------------------- INITIALIZING")
		r.html.render(scrolldown=8, sleep=3)

		print("Status:", r.status_code)

		items = r.html.xpath('//*[@id="site-content"]/div[2]/div[2]/div/div/div/div/div', first=True)

		print("links found: ", len(list(items.absolute_links)))

		df = pd.DataFrame(columns=["Link", "Comuna", "Camas", "Baños", "Capacidad", "Habitaciones", "Precio", "Nota", "Nnota",
							"Descripción", "Titulo1", "Titulo2", "Servicios", "Anfitrion", "Registro", "Ubides", "Ubicacion", "Tipo"])
		count = 0
		try:
			for n in range(0,15,1):
				try:
					print("scrapping info page ", n+1)
					for link in items.absolute_links:
						try:
							print(link)
							r = s.get(link)
							r.html.render(scrolldown=15, sleep=2)
							#print(type(r.html.render(scrolldown=1, sleep=5)))
							#with open(r"C:\Users\Luciano Carvajal\Documents\ESTUDIOS\UFRO\ULS\Webscrapper arriendos\file.html", 
							#            "w", encoding='utf-8') as file:
							#    file.write(r.html.html)
							Link = {"Link":link}
							Comuna = {"Comuna": r.html.xpath('//*[@id="site-content"]/div/div[1]/div[1]/div[1]/div/div/div/div/section/div[2]/div[1]/span/button/span/text()')}
							Camas = {"Camas": r.html.xpath('//*[@id="site-content"]/div/div[1]/div[3]/div/div[1]/div/div[1]/div/div/section/div/div/div/div[1]/ol/li[3]/span[2]/text()')}
							Baños = {"Baños":r.html.xpath('//*[@id="site-content"]/div/div[1]/div[3]/div/div[1]/div/div[1]/div/div/section/div/div/div/div[1]/ol/li[4]/span[2]/text()')}
							Capacidad = {"Capacidad":r.html.xpath('//*[@id="site-content"]/div/div[1]/div[3]/div/div[1]/div/div[1]/div/div/section/div/div/div/div[1]/ol/li[1]/span[1]/text()')}
							Habitaciones = {"Habitaciones":r.html.xpath('//*[@id="site-content"]/div/div[1]/div[3]/div/div[1]/div/div[1]/div/div/section/div/div/div/div[1]/ol/li[2]/span[2]/text()')}
							Precio = {"Precio":r.html.xpath('//*[@id="site-content"]/div/div[1]/div[3]/div/div[2]/div/div/div[1]/div/div/div/div/div/div/div[1]/div[1]/div[1]/div/span/div/span[1]/text()')}
							Nota = {"Nota":r.html.xpath('//*[@id="site-content"]/div/div[1]/div[3]/div/div[2]/div/div/div[1]/div/div/div/div/div/div/div[1]/div[1]/div[2]/span/span[2]/text()')}
							Nnota = {"Nnota":r.html.xpath('//*[@id="site-content"]/div/div[1]/div[3]/div/div[2]/div/div/div[1]/div/div/div/div/div/div/div[1]/div[1]/div[2]/span/span[3]/button/span/text()')}
							Descripción = {"Descripción":r.html.xpath('//*[@data-section-id="DESCRIPTION_DEFAULT"]/div/div/span/span/text()')}
							Titulo1 = {"Titulo1":r.html.xpath('//*[@id="site-content"]/div/div[1]/div[1]/div[1]/div/div/div/div/section/div[1]/span/h1/text()')}
							Titulo2 = {"Titulo2":r.html.xpath('//*[@id="site-content"]/div/div[1]/div[3]/div/div[1]/div/div[1]/div/div/section/div/div/div/div[1]/div/h2/text()')}
							Servicios = {"Servicios":r.html.xpath('//*[@data-section-id="AMENITIES_DEFAULT"]/section/div[3]/div')}
							Anfitrion = {"Anfitrion":r.html.xpath('//*[@id="site-content"]/div/div[1]/div[6]/div/div/div/div[2]/div/section/div[1]/div[2]/h2/text()')}
							Registro = {"Registro":r.html.xpath('//*[@id="site-content"]/div/div[1]/div[6]/div/div/div/div[2]/div/section/div[1]/div[2]/div/ol/li/text()')}
							Ubides = {"Ubides":r.html.xpath('//*[@id="site-content"]/div/div[1]/div[5]/div/div/div/div[2]/div/section/div[4]/div/div/div/div[2]/span/span/text()')}
							Ubicacion = {"Ubicacion":r.html.xpath('//*[@class="gm-style"]/div/div/a/@href')}
							dicts = [Link, Camas, Baños, Capacidad, Habitaciones, Precio, Nota, Nnota,
									Descripción, Titulo1, Titulo2, Servicios, Anfitrion, Registro, Ubides, Ubicacion]
							for dic in dicts:
								Comuna.update(dic)

							dfmin = pd.DataFrame([Comuna])
							df = pd.concat([df, dfmin], ignore_index=True)
						except:
							print("ERROR ON PAGE ", n+1, "\n LINK ", link, "\n CONTINUING SCRAPPING                                     ****   ****   ****")
							time.sleep(60)
										
						
					count += 1
					print("pag", count, " lista")
					if count == 15:
						break
					
					print("rendering again page ", count)
					r = s.get(url)
					r.html.render(scrolldown=8, sleep=4)
					print("Status:", r.status_code)
					button = r.html.xpath('//*[@aria-label="Siguiente"]/@href', first=True)
					print("next button found")
					next_url = "https://www.airbnb.cl" + button
					#print(next_url)
					r = s.get(next_url)
					url = next_url
					print("rendering next page \n\n\n\nRendering page ", count+1, " ---------------------------------------")
					print(url)
					r.html.render(scrolldown=8, sleep=4)
					print("Status: ", r.status_code)

					items = r.html.xpath('//*[@id="site-content"]/div[2]/div[2]/div/div/div/div/div', first=True)
					print("links found: ", len(list(items.absolute_links)))
					
				except: 
					print("ERROR EN PAG ", count+1)
					print(f"C:/Users/bigdatauls/Documents/workspace/python/Webscrapper_arriendos/AirbnbCoquimbopruebacheeckpoint{z}.csv")
					df.to_csv(f"C:/Users/bigdatauls/Documents/workspace/python/Webscrapper_arriendos/AirbnbCoquimbopruebacheeckpoint{z}.csv")
					print("CHECKPOINT CSV EXPORTED")
					time.sleep(100)
					print("CONTINUING FOR LOOP")
					
					count += 1
					print("pag", count, " saltada")
					if count == 15:
						break
					
					print("rendering again page ", count)
					#print(url)
					r = s.get(url)
					r.html.render(scrolldown=8, sleep=4)
					print("Status:", r.status_code)
					button = r.html.xpath('//*[@aria-label="Siguiente"]/@href', first=True)
					print("next button found")
					next_url = "https://www.airbnb.cl" + button
					#print(next_url)
					r = s.get(next_url)
					url = next_url
					print("rendering next page \n\nRendering page ", count+1, " ---------------------------------------")
					#print(url)
					r.html.render(scrolldown=8, sleep=4)
					print("Status: ", r.status_code)

					items = r.html.xpath('//*[@id="site-content"]/div[2]/div[2]/div/div/div/div/div', first=True)
					print("links found: ", len(list(items.absolute_links)))
				

			df.to_csv(f"C:/Users/bigdatauls/Documents/workspace/python/Webscrapper_arriendos/AirbnbCoquimboprueba{z}.csv")
			print(f"C:/Users/bigdatauls/Documents/workspace/python/Webscrapper_arriendos/AirbnbCoquimboprueba{z}.csv")
			print("FINAL CSV EXPORTED")
		except:
			print("MASTER KILLING ERROR ON PAGE ", count+1)
			print(f"C:/Users/bigdatauls/Documents/workspace/python/Webscrapper_arriendos/AirbnbCoquimbopruebakillerror{z}.csv") 
			df.to_csv(f"C:/Users/bigdatauls/Documents/workspace/python/Webscrapper_arriendos/AirbnbCoquimbopruebakillerror{z}.csv")
			print("KILL ERROR CSV EXPORTED")
			time.sleep(60)
	except: 
		print("\n\n\nERROR DE ITERACIÓN, CONTINUANDO FOR LOOP\n\n\n")
		time.sleep(60)
"""

""" LINKS PARA FILTROS
Depas de La Serena, 3 habitaciones, linea playa
https://www.airbnb.cl/s/La-Serena--Chile/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&price_filter_input_type=0&price_filter_num_nights=5&query=La%20Serena%2C%20Chile&date_picker_type=calendar&source=structured_search_input_header&search_type=filter_change&place_id=ChIJyfOJk2TKkZYRy0zY0bOHF4o&l2_property_type_ids%5B%5D=3&kg_and_tags%5B%5D=Tag%3A789&min_bedrooms=3
Depas de La Serena, 2 habitaciones, 2 baños, 2 camas, linea playa
https://www.airbnb.cl/s/La-Serena--Chile/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&price_filter_input_type=0&price_filter_num_nights=5&query=La%20Serena%2C%20Chile&date_picker_type=calendar&source=structured_search_input_header&search_type=filter_change&place_id=ChIJyfOJk2TKkZYRy0zY0bOHF4o&l2_property_type_ids%5B%5D=3&kg_and_tags%5B%5D=Tag%3A789&min_bedrooms=2&min_bathrooms=2&min_beds=2
Depas de La Serena


"""



for z in range(15,50,1): 
	try:
		print(f"\n\n\nINICIANDO PRUEBA COQUIMBOREGION {z} --------------------------------------------------- \n\n")
		#print(f"C:/Users/bigdatauls/Documents/workspace/python/Webscrapper_arriendos/AirbnbLaSerenapruebacheeckpoint{z}.csv")
		#print(f"C:/Users/bigdatauls/Documents/workspace/python/Webscrapper_arriendos/AirbnbLaSerenaprueba{z}.csv")
		#print(f"C:/Users/bigdatauls/Documents/workspace/python/Webscrapper_arriendos/AirbnbLaSerenapruebakillerror{z}.csv")

		url = "https://www.airbnb.cl/s/Coquimbo-Region--Chile/homes?adults=1"
		s = HTMLSession()
		r = s.get(url)
		print("Rendering initial url ---------------------------- INITIALIZING")
		r.html.render(scrolldown=8, sleep=3)

		print("Status:", r.status_code)

		items = r.html.xpath('//*[@id="site-content"]/div[2]/div[2]/div/div/div/div/div', first=True)

		print("links found: ", len(list(items.absolute_links)))

		df = pd.DataFrame(columns=["Link", "Comuna", "Camas", "Baños", "Capacidad", "Habitaciones", "Precio", "Nota", "Nnota",
							"Descripción", "Titulo1", "Titulo2", "Servicios", "Anfitrion", "Registro", "Ubides", "Ubicacion", "Tipo"])
		count = 0
		try:
			for n in range(0,15,1):
				try:
					print("scrapping info page ", n+1)
					for link in items.absolute_links:
						try:
							print(link)
							r = s.get(link)
							r.html.render(scrolldown=15, sleep=2)
							#print(type(r.html.render(scrolldown=1, sleep=5)))
							#with open(r"C:\Users\Luciano Carvajal\Documents\ESTUDIOS\UFRO\ULS\Webscrapper arriendos\file.html", 
							#            "w", encoding='utf-8') as file:
							#    file.write(r.html.html)
							Link = {"Link":link}
							Comuna = {"Comuna": r.html.xpath('//*[@id="site-content"]/div/div[1]/div[1]/div[1]/div/div/div/div/section/div[2]/div[1]/span/button/span/text()')}
							Camas = {"Camas": r.html.xpath('//*[@id="site-content"]/div/div[1]/div[3]/div/div[1]/div/div[1]/div/div/section/div/div/div/div[1]/ol/li[3]/span[2]/text()')}
							Baños = {"Baños":r.html.xpath('//*[@id="site-content"]/div/div[1]/div[3]/div/div[1]/div/div[1]/div/div/section/div/div/div/div[1]/ol/li[4]/span[2]/text()')}
							Capacidad = {"Capacidad":r.html.xpath('//*[@id="site-content"]/div/div[1]/div[3]/div/div[1]/div/div[1]/div/div/section/div/div/div/div[1]/ol/li[1]/span[1]/text()')}
							Habitaciones = {"Habitaciones":r.html.xpath('//*[@id="site-content"]/div/div[1]/div[3]/div/div[1]/div/div[1]/div/div/section/div/div/div/div[1]/ol/li[2]/span[2]/text()')}
							Precio = {"Precio":r.html.xpath('//*[@id="site-content"]/div/div[1]/div[3]/div/div[2]/div/div/div[1]/div/div/div/div/div/div/div[1]/div[1]/div[1]/div/span/div/span[1]/text()')}
							Nota = {"Nota":r.html.xpath('//*[@id="site-content"]/div/div[1]/div[3]/div/div[2]/div/div/div[1]/div/div/div/div/div/div/div[1]/div[1]/div[2]/span/span[2]/text()')}
							Nnota = {"Nnota":r.html.xpath('//*[@id="site-content"]/div/div[1]/div[3]/div/div[2]/div/div/div[1]/div/div/div/div/div/div/div[1]/div[1]/div[2]/span/span[3]/button/span/text()')}
							Descripción = {"Descripción":r.html.xpath('//*[@data-section-id="DESCRIPTION_DEFAULT"]/div/div/span/span/text()')}
							Titulo1 = {"Titulo1":r.html.xpath('//*[@id="site-content"]/div/div[1]/div[1]/div[1]/div/div/div/div/section/div[1]/span/h1/text()')}
							Titulo2 = {"Titulo2":r.html.xpath('//*[@id="site-content"]/div/div[1]/div[3]/div/div[1]/div/div[1]/div/div/section/div/div/div/div[1]/div/h2/text()')}
							Servicios = {"Servicios":r.html.xpath('//*[@data-section-id="AMENITIES_DEFAULT"]/section/div[3]/div')}
							Anfitrion = {"Anfitrion":r.html.xpath('//*[@id="site-content"]/div/div[1]/div[6]/div/div/div/div[2]/div/section/div[1]/div[2]/h2/text()')}
							Registro = {"Registro":r.html.xpath('//*[@id="site-content"]/div/div[1]/div[6]/div/div/div/div[2]/div/section/div[1]/div[2]/div/ol/li/text()')}
							Ubides = {"Ubides":r.html.xpath('//*[@id="site-content"]/div/div[1]/div[5]/div/div/div/div[2]/div/section/div[4]/div/div/div/div[2]/span/span/text()')}
							Ubicacion = {"Ubicacion":r.html.xpath('//*[@class="gm-style"]/div/div/a/@href')}
							dicts = [Link, Camas, Baños, Capacidad, Habitaciones, Precio, Nota, Nnota,
									Descripción, Titulo1, Titulo2, Servicios, Anfitrion, Registro, Ubides, Ubicacion]
							for dic in dicts:
								Comuna.update(dic)

							dfmin = pd.DataFrame([Comuna])
							df = pd.concat([df, dfmin], ignore_index=True)
						except:
							print("ERROR ON PAGE ", n+1, "\n LINK ", link, "\n CONTINUING SCRAPPING                                     ****   ****   ****")
							time.sleep(60)
										
						
					count += 1
					print("pag", count, " lista")
					if count == 15:
						break
					
					print("rendering again page ", count)
					r = s.get(url)
					r.html.render(scrolldown=8, sleep=4)
					print("Status:", r.status_code)
					button = r.html.xpath('//*[@aria-label="Siguiente"]/@href', first=True)
					print("next button found")
					next_url = "https://www.airbnb.cl" + button
					#print(next_url)
					r = s.get(next_url)
					url = next_url
					print("rendering next page \n\n\n\nRendering page ", count+1, " ---------------------------------------")
					print(url)
					r.html.render(scrolldown=8, sleep=4)
					print("Status: ", r.status_code)

					items = r.html.xpath('//*[@id="site-content"]/div[2]/div[2]/div/div/div/div/div', first=True)
					print("links found: ", len(list(items.absolute_links)))
					
				except: 
					print("ERROR EN PAG ", count+1)
					print(f"C:/Users/bigdatauls/Documents/workspace/python/Webscrapper_arriendos/AirbnbCoquimbo-Regionpruebacheeckpoint{z}.csv")
					df.to_csv(f"C:/Users/bigdatauls/Documents/workspace/python/Webscrapper_arriendos/AirbnbCoquimbo-Regionpruebacheeckpoint{z}.csv")
					print("CHECKPOINT CSV EXPORTED")
					time.sleep(100)
					print("CONTINUING FOR LOOP")
					
					count += 1
					print("pag", count, " saltada")
					if count == 15:
						break
					
					print("rendering again page ", count)
					#print(url)
					r = s.get(url)
					r.html.render(scrolldown=8, sleep=4)
					print("Status:", r.status_code)
					button = r.html.xpath('//*[@aria-label="Siguiente"]/@href', first=True)
					print("next button found")
					next_url = "https://www.airbnb.cl" + button
					#print(next_url)
					r = s.get(next_url)
					url = next_url
					print("rendering next page \n\nRendering page ", count+1, " ---------------------------------------")
					#print(url)
					r.html.render(scrolldown=8, sleep=4)
					print("Status: ", r.status_code)

					items = r.html.xpath('//*[@id="site-content"]/div[2]/div[2]/div/div/div/div/div', first=True)
					print("links found: ", len(list(items.absolute_links)))
				

			df.to_csv(f"C:/Users/bigdatauls/Documents/workspace/python/Webscrapper_arriendos/AirbnbCoquimbo-Regionprueba{z}.csv")
			print(f"C:/Users/bigdatauls/Documents/workspace/python/Webscrapper_arriendos/AirbnbCoquimbo-Regionprueba{z}.csv")
			print("FINAL CSV EXPORTED")
			s.cookies.clear()
		except:
			print("MASTER KILLING ERROR ON PAGE ", count+1)
			print(f"C:/Users/bigdatauls/Documents/workspace/python/Webscrapper_arriendos/AirbnbCoquimbo-Regionpruebakillerror{z}.csv") 
			df.to_csv(f"C:/Users/bigdatauls/Documents/workspace/python/Webscrapper_arriendos/AirbnbCoquimbo-Regionpruebakillerror{z}.csv")
			print("KILL ERROR CSV EXPORTED")
			time.sleep(60)
	except: 
		print("\n\n\nERROR DE ITERACIÓN, CONTINUANDO FOR LOOP\n\n\n")
		time.sleep(60)





""" NOTAS : -------------------------------------------------------------------------
Webscrapper
Medir capacidad de recepción de turistas de forma informal

General
Medir capacidad de recepción en 
- Socios de cámara
- Sernatur / No cámara
- Arriendos informales

"""

"""
PAGINAS PARA WEBSCRAPPEAR ------------------------------------------------------------

booking.com
parairnos.cl
yapo.cl
mercadolibre.cl
tripadvisor.cl
portalinmobiliario.com
trovit.cl (mezclados entre permanentes y por día)
booking.com
airbnb.cl
mitula.cl
facebook-marketplace
arriendochile.com
https://chilepropiedades.cl/
"""