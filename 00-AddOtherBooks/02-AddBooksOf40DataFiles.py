# # WARNING - RUN ONLY ONCE, IF RAN TWICE THE SECTIONS JSON WILL BECOME EMPTY SINCE ORIGINAL FILE IS BEING MODIFIED

# import sqlite3
# import json
# from common import query, getCollectionShortName, getArabicNumberWithNumerals



# conn = sqlite3.connect("hadith.db")

# cursor = conn.execute(query)
# dataMap = {}
# hadithMap = {}
# mapForHadithNumber = {}
# for row in cursor:
#     f = open(row[15] + "-" + getCollectionShortName(row[4]) + ".txt", "a")
#     splitArabicNumberList = row[11].split(", ")
#     for splitArabicNumber in splitArabicNumberList:
#         mapForHadithNumber[row[4]] = mapForHadithNumber.get(row[4],0) + 1
#         f.write(str(mapForHadithNumber[row[4]]) + " | " + (row[8] + " " + row[9] + " " + row[10]).replace("\n","<br>")  + "\n")
#         hadithData = {
#             "hadithnumber" : mapForHadithNumber[row[4]], 
#             "arabicnumber" : getArabicNumberWithNumerals(row[11]), # Get a number by changing (a,b,c,d) with (.01,.02,.02,.04)
#             "grades":[],
#             "reference":{
#                         "book":1,
#                         "hadith": getArabicNumberWithNumerals(row[11])
#                     }
#         }
#         if(row[4]) in hadithMap:
#             hadithMap[row[4]].append(hadithData)
#         else:
#             hadithMap[row[4]] = [hadithData]
#     dataMap[getCollectionShortName(row[4])] = {
#         "metadata" : {
#             "name": row[4],
#             "sections":{},
#             "last_hadithnumber": row[6],
#             "section_details": {}
#         },
#         "hadiths": hadithMap.get(row[4])
#     }
#     f.close()

# # print(dataMap)
# inputFile = open('./hadith-api/info.json','r+',encoding="utf-8")
# data : dict = json.load(inputFile)

# for collectionName, collectionDetails in dataMap.items():
#     data[collectionName] = collectionDetails

# inputFile.seek(0)
# inputFile.write(json.dumps(data, indent=4 ,separators=(',', ':'), ensure_ascii=False))
# inputFile.truncate()
# inputFile.close