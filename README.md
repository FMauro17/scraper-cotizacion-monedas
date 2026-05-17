# Scraper de Cotización de Monedas - InvertirOnline

## Descripción
Scraper desarrollado en Python que extrae automáticamente la cotización 
de monedas del mercado argentino desde la página de InvertirOnline y 
genera un DataFrame con los datos obtenidos.

## Tecnologías utilizadas
- Python 3.13
- BeautifulSoup4 - para el web scraping
- Requests - para las solicitudes HTTP
- Pandas - para la creación del DataFrame
- Docker - para la containerización del script

## Estructura del proyecto
scraper-cotizacion-monedas/
├── scraper_monedas.py    # Script principal de extracción
├── Dockerfile            # Configuración del contenedor Docker
├── requirements.txt      # Dependencias del proyecto
└── README.md             # Documentación

## Datos extraídos
El scraper extrae las siguientes columnas:
- **moneda** - Nombre de la moneda
- **compra** - Precio de compra
- **venta** - Precio de venta
- **fecha** - Fecha y hora de la cotización
- **variacion** - Variación porcentual
- **timestamp** - Momento exacto del scraping en UTC

## Cómo ejecutar

### Ejecución local
```bash
pip install -r requirements.txt
python scraper_monedas.py
```

### Ejecución con Docker
```bash
docker build -t scraper-monedas .
docker run --rm scraper-monedas
```

## Autor
Mauro Filani - Data Engineering - Mayo 2026