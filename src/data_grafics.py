import duckdb
import pandas as pd

con = duckdb.connect("data/base_card.duckdb")

top_cards = con.execute("SELECT nombreentidad, SUM(total_tarjetas) as cantidad " \
                        "FROM datos " \
                        "GROUP BY nombreentidad " \
                        "ORDER BY cantidad DESC " \
                        "LIMIT 10").df()
pd.set_option('display.float_format', '{:.0f}'.format)

print(top_cards)