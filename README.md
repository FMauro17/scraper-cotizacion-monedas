# Scraper de Cotización de Monedas - InvertirOnline

## Descripción

Scraper desarrollado en Python que extrae automáticamente la cotización de monedas del mercado argentino desde la página de InvertirOnline, procesa los datos con Pandas y los persiste en una base de datos **PostgreSQL** corriendo en Docker. Incluye pgAdmin para inspección visual de los datos.

---

## Tecnologías utilizadas

| Tecnología | Versión | Rol |
|---|---|---|
| Python | 3.13 | Lenguaje principal |
| BeautifulSoup4 | 4.14.3 | Web scraping / parsing HTML |
| Requests | 2.34.2 | Solicitudes HTTP |
| Pandas | 3.0.3 | Procesamiento y limpieza de datos |
| psycopg2-binary | 2.9.12 | Conector Python → PostgreSQL |
| python-dotenv | 1.2.2 | Manejo de variables de entorno |
| PostgreSQL | 17-alpine | Base de datos relacional (vía Docker) |
| Docker + Docker Compose | — | Orquestación de servicios |
| pgAdmin 4 | latest | Interfaz web para administrar PostgreSQL |

---

## Requisitos previos

Antes de ejecutar el proyecto, asegurate de tener instalado:

- **Python 3.13** — [python.org/downloads](https://www.python.org/downloads/)
- **Docker Desktop** — [docker.com/get-started](https://www.docker.com/get-started/) (incluye Docker Compose)
- **Git** — para clonar el repositorio

Verificá las instalaciones con:
```bash
python --version
docker --version
docker compose version
```

---

## Estructura del proyecto

```
scraper-cotizacion-monedas/
├── scraper_monedas.py    # Script principal: scraping, limpieza e inserción en DB
├── docker-compose.yml    # Orquesta PostgreSQL (puerto 5433) y pgAdmin (puerto 5434)
├── requirements.txt      # Dependencias del proyecto
├── .env                  # Variables de entorno (NO subir a git)
└── README.md             # Documentación
```

---

## Configuración

### 1. Clonar el repositorio

```bash
git clone https://github.com/mauroapple/scraper-cotizacion-monedas.git
cd scraper-cotizacion-monedas
```

### 2. Crear el archivo `.env`

```bash
# .env
DB_PASSWORD=postgres
```

> Si no se define `DB_PASSWORD`, Docker Compose usará `postgres` como valor por defecto.

---

## Infraestructura con Docker Compose

El archivo `docker-compose.yml` levanta dos servicios:

| Servicio | Imagen | Puerto local | Descripción |
|---|---|---|---|
| `postgres` | `postgres:17-alpine` | `5433` | Base de datos PostgreSQL |
| `pgadmin` | `dpage/pgadmin4:latest` | `5434` | Interfaz web de administración |

### Levantar los servicios

```bash
docker compose up -d
```

### Acceder a pgAdmin

1. Abrí el navegador en **http://localhost:5434**
2. Ingresá con:
   - Email: `admin@admin.com`
   - Contraseña: `admin123`
3. Registrá un nuevo servidor con los datos:
   - Host: `postgres` (nombre del servicio en la red Docker)
   - Puerto: `5432`
   - Base de datos: `cotizaciones_db`
   - Usuario: `postgres`
   - Contraseña: el valor de `DB_PASSWORD`

### Detener los servicios

```bash
docker compose down
```

---

## Ejecución del scraper

### Opción A — Entorno virtual (desarrollo local)

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python scraper_monedas.py
```

### Opción B — Docker (sin Python local)

```bash
docker build -t scraper-monedas .
docker run --rm --network=host scraper-monedas
```

> Asegurate de que los contenedores de Docker Compose estén corriendo antes de ejecutar el scraper.

---

## Patrón de carga: TRUNCATE-before-INSERT

Para garantizar idempotencia en cada ejecución, el scraper implementa el patrón **TRUNCATE → INSERT**:

```python
# Limpia la tabla antes de insertar para evitar duplicados
cursor.execute("TRUNCATE TABLE cotizaciones RESTART IDENTITY")

# Inserta los datos frescos del DataFrame
for index, fila in df.iterrows():
    cursor.execute("""
        INSERT INTO cotizaciones (moneda, compra, venta, fecha, variacion, timestamp)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (fila["moneda"], fila["compra"], fila["venta"],
          fila["fecha"], fila["variacion"], fila["timestamp"]))

conn.commit()
```

**Por qué este patrón:**

- Cada corrida del scraper refleja el estado actual del mercado, no una acumulación histórica.
- `RESTART IDENTITY` resetea el contador del `id SERIAL` para mantener los IDs limpios.
- Evita lógicas complejas de deduplicación (`ON CONFLICT`, `UPSERT`) para un caso de uso donde solo importa la última foto del mercado.

---

## Datos extraídos

El scraper captura las siguientes columnas de la tabla de InvertirOnline:

| Columna | Descripción |
|---|---|
| `moneda` | Nombre de la moneda (ej: Dólar Oficial, Euro) |
| `compra` | Precio de compra |
| `venta` | Precio de venta |
| `fecha` | Fecha y hora de la cotización publicada en el sitio |
| `variacion` | Variación porcentual respecto al día anterior |
| `timestamp` | Momento exacto del scraping en UTC |

---

## Ejemplo de output

```
Codigo de respuesta: 200
Tabla encontrada: True
Filas extraidas: 12
Conexion a PostgreSQL exitosa
Tabla cotizaciones lista

               moneda   compra     venta        fecha variacion                 timestamp
0       Dólar Oficial  1010.00   1060.00  12/06/2026     +0.50% 2026-06-12 14:23:07+00:00
1    Dólar Blue/Negro  1280.00   1300.00  12/06/2026     -0.77% 2026-06-12 14:23:07+00:00
2     Dólar Bolsa/MEP  1255.40   1258.30  12/06/2026     +1.12% 2026-06-12 14:23:07+00:00
3     Dólar CCL/Cable  1270.10   1275.80  12/06/2026     +0.90% 2026-06-12 14:23:07+00:00
4            Euro BNA  1105.00   1155.00  12/06/2026     +0.30% 2026-06-12 14:23:07+00:00
5           Real BNA    180.00    195.00  12/06/2026     -0.15% 2026-06-12 14:23:07+00:00
...

Datos insertados correctamente en PostgreSQL
```

---

## Autor

Mauro Filani — Data Engineering — Mayo 2026
