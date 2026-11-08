import pandas as pd
from sodapy import Socrata
from pathlib import Path
import time
import requests


client = Socrata("www.datos.gov.co", None, timeout=60)

carpeta = Path("data")
carpeta.mkdir(exist_ok=True)

max_reintentos = 5
page_size = 5000
FORZAR_TEXTO = ["codigoentidad", "cod_uca"]

def download_page(offset, page_size, max_reintentos=5):
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

# Detect and convert type
def detect_type(serie, umbral=0.95):
    no_null = serie.dropna()
    no_null = no_null[no_null.astype(str).str.strip() != ""]
    if no_null.empty:
        return "texto"

    numeric = pd.to_numeric(no_null, errors='coerce')
    if numeric.notna().mean() >= umbral:
        return "numerico"

    date = pd.to_datetime(no_null, errors="coerce", format="ISO8601")
    if date.notna().mean() >= umbral:
        return "fecha"

    return "texto"

def convert_types(df, umbral=0.95, forzar_texto=()):
    types = {}
    for col in df.columns:
        tipo = "texto" if col in forzar_texto else detect_type(df[col], umbral)
        types[col] = tipo

        if tipo == "numerico":
            df[col] = pd.to_numeric(df[col], errors='coerce')
        elif tipo == "fecha":
            df[col] = pd.to_datetime(df[col], errors='coerce', format="ISO8601")
        else:
            df[col] = df[col].astype("string")

    return df, types

############## Download ####################

results = []
offset = 0

while True:
    batch = download_page(offset, page_size, max_reintentos)
    if not batch:
        break
    results.extend(batch)
    offset += page_size


#################### Procesing #########################

results_df = pd.DataFrame.from_records(results)
results_df.columns = results_df.columns.str.lower()

results_df, types = convert_types(results_df, forzar_texto=FORZAR_TEXTO)

print("Tipos de datos detectados:")
for col, tipo in types.items():
    print(f"{col}: {tipo}")

######### Save ###############
results_df.to_parquet(carpeta / "data.parquet", engine="pyarrow", compression="zstd", index=False)
print(results_df.head())
print(results_df.dtypes)