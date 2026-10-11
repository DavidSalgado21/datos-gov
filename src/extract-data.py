import pandas as pd
from sodapy import Socrata
from pathlib import Path

client = Socrata("www.datos.gov.co", None, timeout=60)

results = []
page_size = 5000
offset = 0

while True:
    batch = client.get("h2jg-r3zg", offset=offset, limit=page_size, order=":id")
    if not batch:
        break
    results.extend(batch)
    offset += page_size

results_df = pd.DataFrame.from_records(results)
results_df.columns = results_df.columns.str.lower()  # Convert column names to lowercase
results_df.to_parquet("data.parquet", compression="zstd", index=False )

# Save the DataFrame to a Parquet file
results_df["tipoentidad"] = pd.to_numeric(results_df["tipoentidad"], errors = 'coerce')
results_df["codigoentidad"] = pd.to_numeric(results_df["codigoentidad"], errors = 'coerce')
results_df["fechacorte"] = pd.to_datetime(results_df["fechacorte"])
results_df["cod_uca"] = pd.to_numeric(results_df["cod_uca"], errors = 'coerce')
results_df["subcuenta"] = pd.to_numeric(results_df["subcuenta"], errors = 'coerce')
results_df["persona_natural"] = pd.to_numeric(results_df["persona_natural"], errors = 'coerce')
results_df["persona_juridica"] = pd.to_numeric(results_df["persona_juridica"], errors = 'coerce')
results_df["total_tarjetas"] = pd.to_numeric(results_df["total_tarjetas"], errors = 'coerce')
results_df.to_parquet("data.parquet", engine="pyarrow", compression="zstd", index=False)
print(results_df.head())