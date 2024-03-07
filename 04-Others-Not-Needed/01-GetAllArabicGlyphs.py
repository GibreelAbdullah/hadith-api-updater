# WARNING - RUN ONLY ONCE, IF RAN TWICE THE SECTIONS JSON WILL BECOME EMPTY SINCE ORIGINAL FILE IS BEING MODIFIED

import sqlite3

conn = sqlite3.connect("../hadith-search-api/hadith_search_full.db")

cursor = conn.execute(
    '''SELECT
	text
from
	hadith h
where
    language = 'ara'
'''
)

s = set()

for row in cursor:
    for character in row[0]:
        s.add(character)

print(s)