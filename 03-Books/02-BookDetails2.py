# REQUIRED - This program will populate the sections (the books in a hadith collection) with the min and max hadith numbers.
# This script iterates through each hadith for each book and records the minimum and maximum hadith number.
# But this approach is causing issues due to data quality. Eg- Muslim Book 5 has hadith 33 in after hadith 657.
# Better approach would be to just take the first and the last as min and max for each book.
import json


def getHadithNumber(hadith):
    if "arabicnumber" in hadith:
        return int(float(hadith["arabicnumber"]))
    return hadith["hadithnumber"]


inputFile = open("./hadith-api/info.json", "r", encoding="utf-8")
info = json.load(inputFile)

bookList = {}

currentBook = ""

for infoCollectionName, infoCollectionDetails in info.items():
    outputFile = open("./hadith-api-master/updates/sections/" +
                      infoCollectionName + ".min.json", "w", encoding="utf-8")
    
    if (infoCollectionDetails["metadata"]["sections"] == {}):
        continue
    bookList = {
        "name": infoCollectionDetails["metadata"]["name"],
        "books": infoCollectionDetails["metadata"]["sections"],
    }
    
    for section_id in list(bookList["books"]):
        if (infoCollectionDetails["metadata"]["section_details"].get(section_id,"") != ""):    
            bookList["books"][section_id]["minHadith"] = infoCollectionDetails["metadata"]["section_details"][section_id]["hadithnumber_first"]
            bookList["books"][section_id]["maxHadith"] = infoCollectionDetails["metadata"]["section_details"][section_id]["hadithnumber_last"]
        else:
            bookList["books"].pop(section_id)
    # chapterObject = {}
    # minHadithNumber = 99999
    # maxHadithNumber = -99999
    # for infoHadith in infoCollectionDetails["metadata"]:
    #     bookList["books"][str(infoHadith["reference"]["book"])]["maxHadith"]
        # if (infoCollectionName + " - " + str(infoHadith["reference"]["book"])) in chapterObject:
        #     if (chapterObject[infoCollectionName + " - " + str(infoHadith["reference"]["book"])][0] < infoHadith["hadithnumber"]):
        #         bookList["books"][str(infoHadith["reference"]["book"])]["maxHadith"] = getHadithNumber(infoHadith)
        #         chapterObject[infoCollectionName + " - " +
        #                       str(infoHadith["reference"]["book"])][1] = getHadithNumber(infoHadith)
                
        #     if (chapterObject[infoCollectionName + " - " + str(infoHadith["reference"]["book"])][0] > infoHadith["hadithnumber"]):
        #         bookList["books"][str(infoHadith["reference"]["book"])]["minHadith"] = getHadithNumber(infoHadith)
        #         chapterObject[infoCollectionName + " - " +
        #                       str(infoHadith["reference"]["book"])][0] = getHadithNumber(infoHadith)
        # else:
        #     # print("--------------" + str(hadith["reference"]["book"]))
        #     # print(bookList)
        #     bookList["books"][str(infoHadith["reference"]["book"])]["minHadith"] = getHadithNumber(infoHadith)
        #     bookList["books"][str(infoHadith["reference"]["book"])]["maxHadith"] = getHadithNumber(infoHadith)

        #     chapterObject[infoCollectionName + " - " + str(infoHadith["reference"]["book"])] = [
        #         getHadithNumber(infoHadith), getHadithNumber(infoHadith)]
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
    outputFile.write(json.dumps(bookList, separators=(',', ':'), ensure_ascii=False))
    outputFile.close()