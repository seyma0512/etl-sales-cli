# etl-sales-cli

[English version](README.md)

Herramienta de línea de comandos (ETL) que limpia datos de ventas desordenados en archivos CSV, los valida y exporta el resultado a CSV y Parquet.

> **Estado:** en desarrollo temprano. El proyecto se construye por etapas, siguiendo el curso *Ingeniería de Datos* (Módulo 1: Python y manipulación de datos).

## Objetivos

- Cargar un CSV crudo con formatos inconsistentes (fechas, números, categorías, duplicados y nulos).
- Limpiar y normalizar los datos con reglas explícitas y documentadas.
- Marcar valores atípicos con el método IQR, sin borrarlos en silencio.
- Exportar el resultado a CSV y Parquet.
- Ejecutar todo desde la terminal, para que después pueda correr en un servidor sin interfaz gráfica.

## Etapas planificadas

1. Generar un CSV de ventas desordenado y sintético para pruebas.
2. Cargar y normalizar los datos con pandas.
3. Limpiar y transformar (duplicados, nulos, categorías, `groupby`, `merge`).
4. Cálculos vectorizados con NumPy.
5. Estadística descriptiva y detección de outliers con IQR.
6. Análisis exploratorio en un notebook de Jupyter.
7. Exportar a CSV y Parquet.
8. Empaquetar todo en una CLI reutilizable.

## Estructura del proyecto

```
etl-sales-cli/
├── etl_sales_cli/     # paquete con el código del pipeline
├── data/
│   ├── raw/           # archivos CSV de entrada (no se versionan)
│   └── processed/     # resultados limpios (no se versionan)
├── notebooks/         # notebooks de análisis exploratorio
├── tests/             # pruebas unitarias
├── requirements.txt
└── README.md
```

## Instalación

Requiere Python 3.11 o superior.

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Uso

Aún no está implementado. La interfaz planeada es:

```powershell
python -m etl_sales_cli data/raw/sales_messy.csv --output data/processed/sales_clean
```

## Licencia

MIT. Ver [LICENSE](LICENSE).
