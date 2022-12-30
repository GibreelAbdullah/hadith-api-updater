# WARNING - RUN ONLY ONCE, IF RAN TWICE THE SECTIONS JSON WILL BECOME EMPTY SINCE ORIGINAL FILE IS BEING MODIFIED

import sqlite3
import json

conn = sqlite3.connect("hadith.db")

def getCollectionFullName(shortName):
	mapping = {
		"bukhari": "Sahih al Bukhari",
		"muslim": "Sahih Muslim",
		"nasai": "Sunan an Nasai",
		"abudawud": "Sunan Abu Dawud",
		"tirmidhi": "Jami At Tirmidhi",
		"ibnmajah": "Sunan Ibn Majah",
		"malik": "Muwatta Malik",
	}
	return mapping.get(shortName, " ")


def getDBData(shortName):
	fullName = getCollectionFullName(shortName)
	query = '''
			SELECT
					c.title_en collection_title,
					h.book_id,
					h.order_in_book,
					b.title_en book_name,
					c2.title ara_ch_name,
					c2.title_en eng_ch_name,
					CASE
						h.chapter_id - h.prev_chapter_id
					when 0 then 0
						else 1
					end is_first_hadith_of_chapter
				from
					(
					SELECT
						h.collection_id,
						h.book_id,
						h.chapter_id,
						LAG ( h.chapter_id,
						1,
						0 ) OVER (
					ORDER BY
						collection_id,
						book_id ,
						order_in_book  
					) prev_chapter_id,
						h.order_in_book
					from
						hadith h
						) h
				inner  join collection c on
						c.id = h.collection_id
				left outer join book b on
						b.collection_id = h.collection_id
						and b.id = h.book_id
				left outer JOIN chapter c2 on
						c2.collection_id = h.collection_id
					and 
						c2.book_id = h.book_id
					and
						c2.id = h.chapter_id
				where c.title_en = "''' + fullName + '''"
			'''
	cursor = conn.execute(query)
	return cursor.fetchall()

file = open('../../hadith-api/info.json', 'r+', encoding="utf-8")
data = json.load(file)

for collectionName, collectionDetails in data.items():
	i=0
	j=0
	prev_book = -1
	chapterNumber = 0
	dbData = getDBData(collectionName)
	# print(dbData)
	while(i < len(dbData)):
	# for row in getDBData(collectionName):
		# for hadith in data[collectionName]["hadiths"]:
		# print("Previous Book Number : ", prev_book)
		# print("Current book number in json : ",
		# 		data[collectionName]["hadiths"][j]["reference"]["book"])
		# print("Current book number in db : ",  dbData[i][1])
		# print("Current hadith number in json : ",
		# 		data[collectionName]["hadiths"][j]["reference"]["hadith"])
		# print("Current hadith number in db : ",  dbData[i][2])
		if(data[collectionName]["hadiths"][j]["reference"]["hadith"] > dbData[i][2]):
			i = i+1
			continue
		if(data[collectionName]["hadiths"][j]["reference"]["hadith"] > dbData[i][2]):
			j = j+1
			continue
		isFirstBook = dbData[i][6]
		if (dbData[i][4] == "" and dbData[i][5] == ""):
			# print("both Equal")
			isFirstBook = 0
		if (prev_book != data[collectionName]["hadiths"][j]["reference"]["book"]):
			prev_book = data[collectionName]["hadiths"][j]["reference"]["book"]
			chapterNumber = 0
		if (isFirstBook == 1):
			# print(dbData[i][6])
			# print("First book increasing chapter to", chapterNumber+1)
			chapterNumber = chapterNumber + 1

		if (data[collectionName]["hadiths"][j]["reference"]["book"] == dbData[i][1] and data[collectionName]["hadiths"][j]["reference"]["hadith"] == dbData[i][2]):

			# print("----------Chapter Number Calculated", chapterNumber)

			chapterDetails = {
				"id": chapterNumber,
				"ara-name": dbData[i][4],
				"eng_name": dbData[i][5],
				"isFirstHadith": isFirstBook,
			}
			data[collectionName]["hadiths"][j]["chapter"] = chapterDetails
		i = i+1
		j = j+1
file.seek(0)
file.write(json.dumps(data, indent=4, ensure_ascii=False))

file.close
# outputFileMin = open('../../hadith-api/info.min.json','w',encoding="utf-8")
# outputFileMin.write(json.dumps(data, separators=(',', ':'), ensure_ascii=False))

# outputFileMin.close

# print("info.json created")
