import duckdb

con = duckdb.connect("data/base_card.duckdb")

df = con.execute("SELECT * FROM datos").df()
df.to_excel("data/datos_excel.xlsx", index=False)

con.close()