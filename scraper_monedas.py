###### EJERCICIO COTIZACION DE MONEDAS ######

"""
Scraper de cotización de monedas - InvertirOnline
Autor: Filani Mauro
Fecha: Mayo 2026
Descripción: Extrae la cotización de monedas del mercado argentino
             desde la página de InvertirOnline y genera un DataFrame
             con los datos obtenidos.
"""

# IMPORTAMOS LAS LIBRERIAS NECESARIAS:
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timezone

# URL DE LA PAGINA QUE VAMOS A SCRAPEAR:
URL = "https://iol.invertironline.com/mercado/cotizaciones/argentina/monedas"

# REALIZAMOS LA SOLICITUD HTTP PARA OBTENER EL HTML DE LA PAGINA:
respuesta = requests.get(URL)

# VERIFICAMOS QUE LA SOLICITUD FUE EXITOSA:
print("Codigo de respuesta:", respuesta.status_code)

# PARSEAMOS EL HTML CON BEAUTIFULSOUP:
soup = BeautifulSoup(respuesta.text, 'html.parser')

# BUSCAMOS LA TABLE DE COTIZACIONES:
tabla = soup.find("table") 

# VERIFICAMOS QUE ENCONTRAMOS LA TABLA:
print("Tabla encontrada:", tabla is not None) 

# CAPTURAMOS EL MOMENTO EXACTO EN QUE REALIZAMOS EL SCRAPING:
timestamp = datetime.now(timezone.utc)

# EXTRAEMOS TODAS LAS FILAS DE LA TABLA:
filas = []
rows = tabla.find_all("tr") 

# RECORREMOS-ITERAMOS CADA FILA SALTANDO LA PRIMERA QUE ES EL ENCABEZADO: 
for row in rows[1:]:
    celdas = row.find_all("td")
    # VERIFICAMOS QUE LA FILA TENGA AL MENOS 5 CELDAS:
    if len(celdas) >= 5:
        moneda = celdas[0].text.strip()
        compra = celdas[1].text.strip()
        venta = celdas[2].text.strip()
        fecha = celdas[3].text.strip()
        variacion = celdas[4].text.strip()

        filas.append({
            "moneda": moneda,
            "compra": compra,
            "venta": venta,
            "fecha": fecha,
            "variacion": variacion,
            "timestamp": timestamp
            
        })
print("Filas extraidas:", len(filas)) 

# CONVERTIMOS LA LISTA DE DICCIONARIOS EN UN DataFrame DE PANDAS:
df = pd.DataFrame(filas)

# LIMPIAMOS LA COLUMNA MONEDA ELIMINANDO SALTOS DE LINEA 
# EL ASTERISCO Y ESPACIOS EXTRAS QUE VIENEN DEL HTML:
df["moneda"] = df["moneda"].str.replace(r'\r\n', '', regex=True)\
                           .str.replace('*', '', regex=False)\
                           .str.strip() 

# REORDENAMOS LAS COLUMNAS PARA QUE MONEDA QUEDE PRIMERA:
df = df[["moneda", "compra", "venta", "fecha", "variacion", "timestamp"]] 

# MOSTRAMOS EL DataFrame COMPLETO:
print(df.to_string()) 

