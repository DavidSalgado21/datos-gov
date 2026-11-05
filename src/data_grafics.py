import duckdb
import pandas as pd

con = duckdb.connect("data/base_card.duckdb")

# TOP 10 BANKS WITH THE MOST CARDS
top_cards_general = con.execute("SELECT nombreentidad, SUM(total_tarjetas) as cantidad " \
                        "FROM datos " \
                        "GROUP BY nombreentidad " \
                        "ORDER BY cantidad DESC " \
                        "LIMIT 10").df()
pd.set_option('display.float_format', '{:.0f}'.format)

top_cards_natural = con.execute("SELECT nombreentidad, SUM(persona_natural) as cantidad" \
                                "FROM datos " \
                                "GROUP BY nombreentidad " \
                                "ORDER BY cantidad DESC " \
                                "LIMIT 10").df()
pd.set_option('display.float_format', '{:.0f}'.format)

top_cards_juridica = con.execute("SELECT nombreentidad, SUM(persona_juridica) as cantidad" \
                                "FROM datos " \
                                "GROUP BY nombreentidad " \
                                "ORDER BY cantidad DESC " \
                                "LIMIT 10").df()
pd.set_option('display.float_format', '{:.0f}'.format)

print(top_cards)