import duckdb
import pandas as pd
import matplotlib.pyplot as plt

con = duckdb.connect("data/base_card.duckdb")

# TOP 10 BANKS WITH THE MOST CARDS
top_cards_general = con.execute("SELECT nombreentidad, SUM(total_tarjetas) as cantidad " \
                        "FROM datos " \
                        "GROUP BY nombreentidad " \
                        "ORDER BY cantidad DESC " \
                        "LIMIT 10").df()
pd.set_option('display.float_format', '{:.0f}'.format)

top_cards_natural = con.execute("SELECT nombreentidad, SUM(persona_natural) as cantidad " \
                                "FROM datos " \
                                "GROUP BY nombreentidad " \
                                "ORDER BY cantidad DESC " \
                                "LIMIT 10").df()
pd.set_option('display.float_format', '{:.0f}'.format)

top_cards_juridica = con.execute("SELECT nombreentidad, SUM(persona_juridica) as cantidad " \
                                "FROM datos " \
                                "GROUP BY nombreentidad " \
                                "ORDER BY cantidad DESC " \
                                "LIMIT 10").df()
pd.set_option('display.float_format', '{:.0f}'.format)


######################## CREATE GRAFICS ##############################

fix, axes = plt.subplots(2, 2, figsize=(16, 10))

# TOP 10 BANKS WITH THE MOST CARDS
axes[0,0].bar(top_cards_general['nombreentidad'], top_cards_general['cantidad'])
axes[0,0].set_title("Top 10 Banks with the Most Cards")
axes[0,0].set_xlabel("Banks")
axes[0,0].set_ylabel("Number of Cards")
axes[0,0].tick_params(axis='x', rotation=45)

# TOP 10 BANKS WITH THE MOST CARDS FOR NATURAL PERSONS
axes[0,1].bar(top_cards_natural['nombreentidad'], top_cards_natural['cantidad'])
axes[0,1].set_title("Top 10 Banks with the Most Cards for natural persons")
axes[0,1].set_xlabel("Banks")
axes[0,1].set_ylabel("Number of Cards")
axes[0,1].tick_params(axis='x', rotation=45)

# TOP 10 BANKS WITH THE MOST CARDS FOR JURIDICAL PERSONS
axes[1,0].bar(top_cards_juridica['nombreentidad'], top_cards_juridica['cantidad'])
axes[1,0].set_title("Top 10 Banks with the Most Cards for juridical persons")
axes[1,0].set_xlabel("Banks")
axes[1,0].set_ylabel("Number of Cards")
axes[1,0].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig("top_10_banks_all.png", dpi=300)
plt.show()