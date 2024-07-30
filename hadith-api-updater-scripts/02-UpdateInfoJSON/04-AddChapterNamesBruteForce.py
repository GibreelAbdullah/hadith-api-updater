# The brute force method

import pickle
import json

"""
def getDBData():
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
					end is_first_hadith_of_chapter,
                    c2.number
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
			'''
    cursor = conn.execute(query)
    return cursor.fetchall()
"""

def removeDecimal(chapterNumber):
    if isinstance(chapterNumber, float):
        return int(chapterNumber)
    else:
        return chapterNumber

def getCollectionFullName(shortName):
    mapping = {
        "bukhari": "Sahih al-Bukhari",
        "muslim": "Sahih Muslim",
        "nasai": "Sunan an-Nasa'i",
        "abudawud": "Sunan Abi Dawud",
        "tirmidhi": "Jami` at-Tirmidhi",
        "ibnmajah": "Sunan Ibn Majah",
        "malik": "Muwatta Malik",
        "musnad": "Musnad Ahmad",
    }
    return mapping.get(shortName, " ")

# reading dbData from the file
with open('./hadith-api-updater-scripts/02-UpdateInfoJSON/dbData.pickle', 'rb') as f:
    dbData = pickle.load(f)

def getChapterDetails(collectionName, hadithReference):
    fullName = getCollectionFullName(collectionName)
    if (fullName != " "):
        bookNumber = hadithReference["book"]
        hadithNumber = hadithReference["hadith"]
        for data in dbData:
            if (data[0] ==  fullName and int(data[1]) == bookNumber and int(data[2]) == hadithNumber):
                return {
                    "id": None if data[7] == '' or data[7] is None else removeDecimal(data[7]),
                    "ara-name": data[4] if data[4] is None else data[4].replace('‏',''),
                    "eng-name": data[5],
                    "isFirstHadith": bool(data[6]),
                }
    return {
        "id": None,
        "ara-name": None,
        "eng_name": None,
        "isFirstHadith": None,
    }


inputFile = open('./hadith-api/info.json', 'r+', encoding="utf-8")
data = json.load(inputFile)

for collectionName, collectionDetails in data.items():
    print(collectionName)
    for hadith in data[collectionName]["hadiths"]:
        hadith["chapter"] = getChapterDetails(collectionName, hadith["reference"])

# inputFile.close
# outputFile = open('./hadith-api/info.json', 'w', encoding="utf-8")

inputFile.seek(0)
inputFile.write(json.dumps(data, indent=4, ensure_ascii=False))
inputFile.truncate()
inputFile.close