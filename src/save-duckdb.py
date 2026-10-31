import duckdb

con = duckdb.connect("data/base_card.duckdb")

con.execute("""
    CREATE OR REPLACE TABLE datos AS
    SELECT * FROM read_parquet('data/data.parquet')
""")

print(con.execute("SELECT * FROM datos LIMIT 5").df())
con.close()