# WARNING - RUN ONLY ONCE, IF RAN TWICE THE SECTIONS JSON WILL BECOME EMPTY SINCE ORIGINAL FILE IS BEING MODIFIED

import sqlite3
import json

conn = sqlite3.connect("../hadith.db")

cursor = conn.execute(
    '''SELECT
	c.name,
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
inputFile = open('../../hadith-api/info.json','r',encoding="utf-8")
data = json.load(inputFile)

for collectionName, collectionDetails in data.items():
    sectionList = {}
    for row in results:
        if(collectionName == row[0]):
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
    data[collectionName]["metadata"]["sections"] = sectionList

inputFile.close

outputFile = open('../../hadith-api/info.json','w',encoding="utf-8")
outputFile.write(json.dumps(data, indent=4, ensure_ascii=False))

outputFileMin = open('../../hadith-api/info.min.json','w',encoding="utf-8")
outputFileMin.write(json.dumps(data, separators=(',', ':'), ensure_ascii=False))

outputFile.close

print("info.json created")
