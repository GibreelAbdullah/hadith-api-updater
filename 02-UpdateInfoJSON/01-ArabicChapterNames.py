# WARNING - RUN ONLY ONCE, IF RAN TWICE THE SECTIONS JSON WILL BECOME EMPTY SINCE ORIGINAL FILE IS BEING MODIFIED

import sqlite3
import json

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
inputFile = open('../hadith-api/info.json','r+',encoding="utf-8")
data = json.load(inputFile)

# TODO: Take section name already in info.json as eng-name and from db as ara-name;
			# CURRENT FORMAT
            # "sections": {
			# 	"0": "",
			# 	"1": "Forty Hadith of Shah Waliullah Dehlawi"
			# },
#  Required Format
            # "sections": {
            #     "0": {
            #         "eng-name": "",
            #         "ara-name": ""
            #       }
            # }
for collectionName, collectionDetails in data.items():
    sectionList = {}
    for row in results:
        # print(collectionName)
        # print(row[0])
        if(getCollectionFullName(collectionName) == row[0]):
            for sectionId, sectionName in data[collectionName]["metadata"]["sections"].items():
                if(sectionName == row[2]):
                    sectionList[sectionId] = {
                        "eng-name" : row[2],
                        "ara-name" : row[1].strip()
                    }
                elif (sectionName == ''):
                    sectionList[sectionId] = {
                        "eng-name" : '',
                        "ara-name" : ''
                    }
                elif (sectionName == 'Introduction'):
                    sectionList[sectionId] = {
                        "eng-name" : 'Introduction',
                        "ara-name" : 'المقدمة'
                    }
                else:
                    sectionList[sectionId] = {
                        "eng-name" : sectionName,
                        "ara-name" : ''
                    }
        else:
            for sectionId, sectionName in data[collectionName]["metadata"]["sections"].items():
                sectionList[sectionId] = {
                        "eng-name" : sectionName,
                        "ara-name" : ''
                    }
    data[collectionName]["metadata"]["sections"] = sectionList

inputFile.seek(0)
inputFile.write(json.dumps(data, indent=4, ensure_ascii=False))
inputFile.truncate()
inputFile.close


outputFileMin = open('../hadith-api/info.min.json','w',encoding="utf-8")
outputFileMin.write(json.dumps(data, separators=(',', ':'), ensure_ascii=False))

outputFileMin.close

print("info.json created")
