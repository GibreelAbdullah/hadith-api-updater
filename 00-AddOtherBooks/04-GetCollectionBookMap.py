import sqlite3

conn = sqlite3.connect("hadith.db")

cursor = conn.execute(
    '''SELECT
	c.title_en,
	b.title,
	b.title_en
from
	collection c
inner join book b on
	c.id = b.collection_id 
order by
	b.collection_id, b.order_in_collection'''
)

results = cursor.fetchall()
map = {}
for row in results:
    if (map.get(row[0]) == None):
        map[row[0]] = {row[2].strip():row[1].strip()}
    else:
        map[row[0]].update({row[2].strip():row[1].strip()})

print(map)