# REQUIRED - This program will populate the sections (the books in a hadith collection) with the min and max hadith numbers.

import json

inputFile = open("../../hadith-api/info.json", "r", encoding="utf-8")
data = json.load(inputFile)

bookList = {}

currentBook = ""
for collectionName, collectionDetails in data.items():
    outputFile = open("../../hadith-api/updates/sections/" + collectionName + ".json", "w", encoding="utf-8")
    bookList = {
        "name": collectionDetails["metadata"]["name"],
        "books": collectionDetails["metadata"]["sections"],
    }
    for hadith in collectionDetails["hadiths"]:
        if "minHadith" in bookList["books"][str(hadith["reference"]["book"])]:
            bookList["books"][str(hadith["reference"]["book"])]["minHadith"] = min(bookList["books"][str(hadith["reference"]["book"])]["minHadith"],hadith["hadithnumber"])
            bookList["books"][str(hadith["reference"]["book"])]["maxHadith"] = max(bookList["books"][str(hadith["reference"]["book"])]["minHadith"],hadith["hadithnumber"])
        else:
            bookList["books"][str(hadith["reference"]["book"])]["minHadith"] = hadith["hadithnumber"]
            bookList["books"][str(hadith["reference"]["book"])]["maxHadith"] = hadith["hadithnumber"]

    # print(bookList)
    outputFile.write(json.dumps(bookList, indent=4, ensure_ascii=False))
    outputFile.close()
