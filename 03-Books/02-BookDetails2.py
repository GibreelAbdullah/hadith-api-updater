# REQUIRED - This program will populate the sections (the books in a hadith collection) with the min and max hadith numbers.
# This script iterates through each hadith for each book and records the minimum and maximum hadith number.
# But this approach is causing issues due to data quality. Eg- Muslim Book 5 has hadith 33 in after hadith 657.
# Better approach would be to just take the first and the last as min and max for each book.
import json


def getHadithNumber(hadith):
    if "arabicnumber" in hadith:
        return int(float(hadith["arabicnumber"]))
    return hadith["hadithnumber"]


inputFile = open("../hadith-api/info.json", "r", encoding="utf-8")
data = json.load(inputFile)

bookList = {}

currentBook = ""

for collectionName, collectionDetails in data.items():
    outputFile = open("../hadith-api/updates/sections/" +
                      collectionName + ".json", "w", encoding="utf-8")
    
    if (collectionDetails["metadata"]["sections"] == {}):
        continue
    bookList = {
        "name": collectionDetails["metadata"]["name"],
        "books": collectionDetails["metadata"]["sections"],
    }

    chapterObject = {}
    minHadithNumber = 99999
    maxHadithNumber = -99999
    for hadith in collectionDetails["hadiths"]:
        if (collectionName + " - " + str(hadith["reference"]["book"])) in chapterObject:
            if (chapterObject[collectionName + " - " + str(hadith["reference"]["book"])][0] < hadith["hadithnumber"]):
                bookList["books"][str(hadith["reference"]["book"])]["maxHadith"] = getHadithNumber(hadith)
                chapterObject[collectionName + " - " +
                              str(hadith["reference"]["book"])][1] = getHadithNumber(hadith)
                
            if (chapterObject[collectionName + " - " + str(hadith["reference"]["book"])][0] > hadith["hadithnumber"]):
                bookList["books"][str(hadith["reference"]["book"])]["minHadith"] = getHadithNumber(hadith)
                chapterObject[collectionName + " - " +
                              str(hadith["reference"]["book"])][0] = getHadithNumber(hadith)
        else:
            # print("--------------" + str(hadith["reference"]["book"]))
            # print(bookList)
            bookList["books"][str(hadith["reference"]["book"])]["minHadith"] = getHadithNumber(hadith)
            bookList["books"][str(hadith["reference"]["book"])]["maxHadith"] = getHadithNumber(hadith)

            chapterObject[collectionName + " - " + str(hadith["reference"]["book"])] = [
                getHadithNumber(hadith), getHadithNumber(hadith)]
        # try:
        #     if "minHadith" in bookList["books"][str(hadith["reference"]["book"])]:
        #         if(minHadithNumber > hadith["hadithnumber"]):
        #             minHadithNumber = hadith["hadithnumber"]
        #             bookList["books"][str(hadith["reference"]["book"])]["minHadith"] = int(float(hadith["arabicnumber"]))
        #         if(maxHadithNumber < hadith["hadithnumber"]):
        #             maxHadithNumber = hadith["hadithnumber"]
        #             bookList["books"][str(hadith["reference"]["book"])]["maxHadith"] = int(float(hadith["arabicnumber"]))
        # except:
        #     if "minHadith" in bookList["books"][str(hadith["reference"]["book"])]:
        #         if(minHadithNumber > hadith["hadithnumber"]):
        #             minHadithNumber = hadith["hadithnumber"]
        #             bookList["books"][str(hadith["reference"]["book"])]["minHadith"] = hadith["hadithnumber"]
        #         if(maxHadithNumber < hadith["hadithnumber"]):
        #             maxHadithNumber = hadith["hadithnumber"]
        #             bookList["books"][str(hadith["reference"]["book"])]["maxHadith"] = hadith["hadithnumber"]
    # print(bookList)
    # print(chapterObject)
    outputFile.write(json.dumps(bookList, indent=4, ensure_ascii=False))
    outputFile.close()
