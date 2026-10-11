# AGENTS.md - Proyecto Webscrapping_INE

## 📋 Visión General del Proyecto

**Web to BI** - Una solución integral de Inteligencia de Negocios que automatiza la extracción, almacenamiento y visualización de datos estratégicos web del **Instituto Nacional de Estadística (INE) Uruguay**.

- **Fuente**: https://www.gub.uy/instituto-nacional-estadistica/comunicacion/publicaciones
- **Destino**: MySQL en AWS RDS
- **Visualización**: Dashboards Power BI
- **Lenguaje**: Python 3.14

---

## 🏗️ Arquitectura

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Selenium   │────▶│  Pandas     │────▶│  SQLAlchemy │────▶│  MySQL/AWS  │
│  WebDriver  │     │  Limpieza   │     │  Motor      │     │  (RDS)      │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
                                                                         │
                                                                         ▼
                                                                ┌─────────────┐
                                                                │  Power BI   │
                                                                │  Dashboards │
                                                                └─────────────┘
```

---

## 📁 Estructura del Repositorio

```
Webscrapping_INE/
├── .gitignore
├── AGENTS.md                 # Este archivo
├── config.py                 # Config estática (URLs, nombres tablas, rutas)
├── main.py                   # Punto entrada - orquesta scraping + almacenamiento
├── requirements.txt          # Dependencias Python
├── README.md                 # Documentación del proyecto
├── dashboard.pbix            # Archivo dashboard Power BI
├── imgs/                     # Imágenes para README
│   ├── ddbb_structure.jpg    # Diagrama esquema BD
│   └── header.jpg
├── power_bi/
│   └── example_script.py     # Script Python para importar datos en Power BI
├── sql/
│   ├── create_tables.sql     # DDL: tablas + claves foráneas
│   ├── fixed_data.sql        # Datos referencia (tablas dimensión)
│   ├── sp_get_data.sql       # Procedimientos almacenados consulta datos
│   └── sp_total_rows.sql     # Procedimiento almacenado conteo filas
└── src/
    ├── utils.py              # Utilidades CLI (entrada usuario, fechas)
    ├── connection/
    │   ├── __init__.py
    │   ├── blueprint.py      # Dataclass Credenciales
    │   └── controller.py     # Motor BD, lógica upsert, stored procs
    └── webscrap/
        ├── __init__.py
        ├── blueprint.py      # Dataclass StoredOutputs
        ├── controller.py     # Orquesta los 3 scrapers
        ├── utils.py          # Validación URL
        ├── ipc.py            # Scraper IPC (Índice Precios Consumo)
        ├── ims.py            # Scraper IMS (Índice Medio Salarios)
        └── iccv.py           # Scraper ICCV (Índice Costo Construcción Vivienda)
```

---

## 🔑 Componentes Clave

### 1. Configuración (`config.py`)

```python
class Rutas(StrEnum):
    ROOT_PATH = os.path.abspath(Path(__file__).resolve().parent)
    INE_URL = "https://www.gub.uy/instituto-nacional-estadistica/comunicacion/publicaciones"

class TableNames(StrEnum):
    IPC = "t_ipc"
    IMS = "t_ims"
    ICCV = "t_iccv"
```

### 2. Punto de Entrada (`main.py`)

```python
# Flujo:
# 1. Imprime cabecera
# 2. Obtiene año/mes del usuario (validado ≤ mes actual)
# 3. Crea motor de BD desde credenciales .env
# 4. Ejecuta controlador de Webscrapping (driver Selenium compartido)
# 5. Persiste cada DataFrame en su tabla correspondiente (INSERT IGNORE)
```

### 3. Conexión a Base de Datos (`src/connection/controller.py`)

- **Credenciales**: Cargadas desde `.env` (HOST, PORT, DATABASE, USER1, PSW1)
- **Motor**: SQLAlchemy con `pool_pre_ping=True`, `future=True`
- **Upsert**: `INSERT IGNORE` vía método personalizado `insert_ignore()` (evita duplicados)
- **Conteo de filas**: Usa procedimiento almacenado `sp_total_rows(tabla, @total)`

### 4. Módulo de Web Scraping (`src/webscrap/`)

Los tres scrapers comparten el mismo patrón:
- Heredan de `dataclass`
- Construyen URL: `{base_url}/{indicador-nombre}-{mes}-{año}`
- Validan URL existe via petición `HEAD`
- Usan driver `Chrome` compartido (pasado desde el controlador)
- Esperan elementos via `WebDriverWait`
- Extraen tablas HTML → `pd.read_html()`
- Limpian/transforman → retornan `DataFrame`

| Scraper | Clase | Patrón URL | Columnas Clave |
|---------|-------|-------------|----------------|
| **IPC** | `IndicePreciosConsumo` | `indice-precios-del-consumo-ipc-{mes}-{año}` | periodo, id_division, ponderacion, indice, var_mensual, var_ac_anual, var_doce_meses, incidencia |
| **IMS** | `IndiceMedioSalarios` | `indice-medio-salarios-ims-{mes}-{año}` | periodo, id_sector, indice, mes, acum_anual, ultimos_doce_meses, incidencias |
| **ICCV** | `IndiceCostoConstruccionVivienda` | `indice-costo-construccion-vivienda-iccv-{mes}-{año}` | periodo, id_rubro, indice, var_mensual, incidencias |

---

## 🗄️ Esquema de Base de Datos

### Tablas Dimensión (Datos de Referencia)
```sql
t_ipc_desc     (id_division TINYINT PK, descripcion VARCHAR(255))
t_ims_desc     (id_sector CHAR(1) PK, descripcion VARCHAR(255))
t_iccv_desc    (id_rubro TINYINT PK, descripcion VARCHAR(255))
```

### Tablas Hecho (Datos Scrapeados)
```sql
t_ipc   (periodo DATE, id_division, ponderacion, indice, var_mensual, var_ac_anual, var_doce_meses, incidencia)
        PK(periodo, id_division), FK → t_ipc_desc

t_ims   (periodo DATE, id_sector, indice, mes, acum_anual, ultimos_doce_meses, incidencias)
        PK(periodo, id_sector), FK → t_ims_desc

t_iccv  (periodo DATE, id_rubro, indice, var_mensual, incidencias)
        PK(periodo, id_rubro), FK → t_iccv_desc
```

Todas las tablas: `ENGINE=InnoDB`, `DECIMAL(18,4)` para métricas, `UNSIGNED` para IDs.

---

## 📦 Procedimientos Almacenados

| Procedimiento | Propósito |
|---------------|-----------|
| `sp_get_ipc()` | Une t_ipc + t_ipc_desc, ordenado por periodo, id_division |
| `sp_get_ims()` | Une t_ims + t_ims_desc, ordenado por periodo, id_sector |
| `sp_get_iccv()` | Une t_iccv + t_iccv_desc, ordenado por periodo, id_rubro |
| `sp_total_rows(tabla, OUT nrows)` | COUNT(*) dinámico para cualquier tabla |

---

## ⚙️ Dependencias (`requirements.txt`)

```
arrow==1.2.3          # Manejo de fechas
pandas==2.3.3         # Manipulación de datos
pyfiglet==1.0.4       # Cabeceras ASCII art
pymysql==1.1.2        # Driver MySQL
python-dotenv==0.21.0 # Carga de .env
requests==2.32.4      # Peticiones HTTP (validación URL)
selenium==4.28.1      # Web scraping
sqlalchemy==2.0.25    # ORM/Motor
```

**Requisito del sistema**: Chrome + ChromeDriver compatible con Selenium 4.28.1

---

## 🚀 Uso

### 1. Configuración Inicial
```bash
# Crear .env en la raíz del proyecto
HOST=tu-endpoint-rds
PORT=3306
DATABASE=INE
USER1=tu-usuario
PSW1=tu-password

# Instalar dependencias
pip install -r requirements.txt

# Crear esquema BD (ejecutar en DBeaver/MySQL Workbench)
# Ejecutar: sql/create_tables.sql → sql/fixed_data.sql → sql/sp_get_data.sql → sql/sp_total_rows.sql
```

### 2. Ejecutar Scraping
```bash
python main.py
# Solicita: Año (≥2023), Mes (1-12, ≤ mes actual)
# Abre Chrome, scrapea 3 indicadores, guarda en AWS
```

### 3. Integración Power BI
1. Abrir Power BI → Obtener datos → Script de Python
2. Pegar/modificar `power_bi/example_script.py`
3. Ejecutar consulta: `CALL sp_get_ipc()` (o ims/iccv)
4. Construir visualizaciones

---

## ⚠️ Notas Importantes

- **Fragilidad**: El scraping depende de la estructura web del INE (XPaths, IDs de tablas). Cambios rompen el scraper.
- **Duplicados**: `INSERT IGNORE` previene errores de PK duplicada en re-ejecuciones.
- **Rango de Fechas**: Solo soporta datos desde 2023 en adelante (validado en `user_year()`).
- **Selenium**: Ejecuta ventana Chrome visible (`--start-maximized`), no headless.
- **AWS**: Requiere VPC/grupo de seguridad permitiendo tu IP al puerto 3306 de RDS.

---

## 🔧 Tareas Comunes de Mantenimiento

| Tarea | Archivos a Modificar |
|-------|---------------------|
| Actualizar URL base INE | `config.py:Rutas.INE_URL` |
| Cambiar nombres de tablas | `config.py:TableNames` |
| Reparar XPath roto | `src/webscrap/{ipc,ims,iccv}.py:xpath` o `table_xpath` |
| Agregar nuevo indicador | Crear scraper en `src/webscrap/`, registrar en `controller.py` y `config.py` |
| Cambios de esquema | `sql/create_tables.sql` + `set_colnames()` del scraper correspondiente |
| Actualizar datos de referencia | `sql/fixed_data.sql` |

---

*Generado para contexto de agentes - mantener actualizado conforme evoluciona el proyecto*