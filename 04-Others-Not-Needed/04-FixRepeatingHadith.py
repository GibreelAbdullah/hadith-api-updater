# WARNING - RUN ONLY ONCE, IF RAN TWICE THE SECTIONS JSON WILL BECOME EMPTY SINCE ORIGINAL FILE IS BEING MODIFIED

import os
import re
import mysql.connector

import json


def getCollectionShortName(fullName):
    mapping = {
        "Sahih al Bukhari": "bukhari",
        "Sahih Muslim": "muslim",
        "Sunan an Nasai": "nasai",
        "Sunan Abu Dawud": "abudawud",
        "Jami At Tirmidhi": "tirmidhi",
        "Sunan Ibn Majah": "ibnmajah",
        "Muwatta Malik": "malik",
    }
    return mapping.get(fullName, " ")


def alphanumericNumbering(sourceNumbering):
    output_string = ""
    for char in sourceNumbering:
        if char.isalpha():
            code = ord(char.lower()) - ord('a') + 1
            replacement = f'.{code:02}'
            output_string += replacement
        else:
            output_string += char
    return output_string


def getTargetNumbering(sourceNumbering):
    targetNumbering = list(map(str.strip, alphanumericNumbering(
        sourceNumbering.replace(' ', '')).split(',')))

    for index, numbering in enumerate(targetNumbering):
        hadithNumber = int(float(targetNumbering[0]))
        if (numbering.startswith('.')):
            targetNumbering[index] = str(hadithNumber) + str(numbering)
    return targetNumbering

# def getTargetHadithNumbering(bookName, targetArabicNumbering):
#     if(bookName not in ("Sahih Muslim","Jami At Tirmidhi")):
#         return targetArabicNumbering
    
#     # Goto info.json for muslim and tirmidhi. 
#     # run a iterator over info.json and targetNumbering
#     # check if info.json 

#     # edge cases. 884.01, .02 are separated from 884.03, 884.04 which are present after 889.
#     # easier option would be to rescrape everything from sunnah.com (or its DB)
#     return []

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="hadith"
)
cursor = mydb.cursor()

# conn = sqlite3.connect("hadith.db")

cursor.execute(
    """SELECT collection, hadithNumber from HadithTable where hadithNumber like '%,%' and collection = 'nasai'"""
)
results = cursor.fetchall()

hadithMapping = {}

path = "/home/alfi/Projects/hadith-api-updater/TempOutput/"
dir_list = os.listdir(path)   

# print(dir_list)

matchingCollections = list(filter(lambda string: "nasai" in string, dir_list))
print(matchingCollections)
for collection in matchingCollections:
    print(collection)    
    inputFile = open(path + collection , 'r+', encoding="utf-8")
    lines = inputFile.readlines()
    for line in lines:
        for row in results:
            sameHadithFlag = False
            for i in range(len(getTargetNumbering(row[1]))):
                # print(str(i) + ":" + getTargetNumbering(row[1])[i] )
                if(i == 0 and line.startswith(getTargetNumbering(row[1])[i] + ' |')):
                    # inputFile.writelines(line)
                    sameHadithFlag = True
                    continue
                elif(sameHadithFlag):
                    inputFile.writelines(getTargetNumbering(row[1])[i] + re.sub(r'^.*?\|', ' |', line))
                i = i + 1
            # if(not sameHadithFlag):
            #     inputFile.writelines(line)
    inputFile.close

# for row in results:
#     targetArabicNumbering = getTargetNumbering(row[1])
#     hadithMapping.setdefault(getCollectionShortName(row[0]), []).append(
#         {
#             "sourceNumbering": row[1],
#             "targetNumbering": {
#                 "targetArabicNumbering": targetArabicNumbering,
#                 # "targetHadithNumbering": getTargetHadithNumbering(row[0],targetArabicNumbering)
#             }
#         }
#     )
  
        


# outputFileMin = open('./output.json', 'w', encoding="utf-8")
# outputFileMin.write(json.dumps(hadithMapping, indent=4,
#                     ensure_ascii=False, separators=(',', ':')))
# # inputFile.write(json.dumps(data, indent=4, ensure_ascii=False))

# outputFileMin.close
