import pandas as pd
from sodapy import Socrata
from pathlib import Path
import time
import requests


client = Socrata("www.datos.gov.co", None, timeout=60)

carpeta = Path("datos")
carpeta.mkdir(exist_ok=True)
max_reintentos = 5

results = []
page_size = 5000
offset = 0

def descargar_pagina(offset, page_size, max_reintentos=5):
    for intento in range(1, max_reintentos + 1):
        try:
            return client.get("h2jg-r3zg", offset=offset, limit=page_size, order=":id")
        except (requests.exceptions.Timeout,
                requests.exceptions.ConnectionError,
                requests.exceptions.HTTPError) as e:
            espera = 2 ** intento
            print(f"Error en offset {offset} (intento {intento}): {e}. Reintento en {espera}s")
            time.sleep(espera)
    raise RuntimeError(f"No se pudo descargar la página con offset={offset}")

# 

while True:
    batch = client.get("h2jg-r3zg", offset=offset, limit=page_size, order=":id")
    if not batch:
        break
    results.extend(batch)
    offset += page_size

results_df = pd.DataFrame.from_records(results)
results_df.columns = results_df.columns.str.lower()  # Convert column names to lowercase
results_df.to_parquet("data/data.parquet", compression="zstd", index=False )

# Save the DataFrame to a Parquet file

def save_dataframe_to_parquet():
    columns_numbers = ["tipoentidad", "codigoentidad", "cod_uca", "subcuenta", "persona_natural", "persona_juridica", "total_tarjetas"]

    results_df[columns_numbers] = results_df[columns_numbers].apply(
        pd.to_numeric, errors='coerce'
    )

results_df["tipoentidad"] = pd.to_numeric(results_df["tipoentidad"], errors = 'coerce')
results_df["codigoentidad"] = pd.to_numeric(results_df["codigoentidad"], errors = 'coerce')
results_df["fechacorte"] = pd.to_datetime(results_df["fechacorte"])
results_df["cod_uca"] = pd.to_numeric(results_df["cod_uca"], errors = 'coerce')
results_df["subcuenta"] = pd.to_numeric(results_df["subcuenta"], errors = 'coerce')
results_df["persona_natural"] = pd.to_numeric(results_df["persona_natural"], errors = 'coerce')
results_df["persona_juridica"] = pd.to_numeric(results_df["persona_juridica"], errors = 'coerce')
results_df["total_tarjetas"] = pd.to_numeric(results_df["total_tarjetas"], errors = 'coerce')
results_df.to_parquet("data/data.parquet", engine="pyarrow", compression="zstd", index=False)
print(results_df.head())