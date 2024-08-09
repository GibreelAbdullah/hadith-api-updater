"""
Script to create databases for each collection

This script uses the hadith api data to create a database for each collection.

The script creates a table in the database with the following columns:

- hadithnumber: the global hadith number
- arabicnumber: the arabic number of the hadith
- text: the text of the hadith
- grades: the grades of the hadith
- bookNumber: the book number of the hadith
- bookhadith: the hadith number within the book
- bookname: the name of the book
- language: the language of the collection
- shortname: the short name of the collection

The script also uses the collections data to normalize the collection names.

"""
import json
import sqlite3
import os

editionsFile = open("../hadith-api/editions.json", "r", encoding="utf-8")
editionsData = json.load(editionsFile)
collectionDict = []

collectionsFile = open("../hadith-api-master/updates/collections/collections.min.json")
collectionsData = json.load(collectionsFile)
print(collectionsData)
collectionShortNameDict = {}
for collectionCategories in collectionsData["collections"]:
    for collectionFileNameObject in collectionCategories["books"]:
        collectionShortNameDict[collectionFileNameObject["eng-name"]] = collectionFileNameObject["name"]

for collectionList, collectionListDetails in editionsData.items():
    for collection in collectionListDetails["collection"]:
        collectionDict.append(
            {"name": collection["name"], "language": collection["name"][:3]}
        )
        path = "data/" + collection["name"]
        if not os.path.exists(path):
            os.makedirs(path)
        conn = sqlite3.connect(path + "/hadith.db")
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS hadith;")
        cursor.execute("CREATE VIRTUAL TABLE IF NOT EXISTS hadith USING FTS5(hadithnumber,arabicnumber,text,grades,bookNumber,bookhadith,bookname,language,shortname, tokenize = 'porter unicode61 remove_diacritics 1');")


            
        # for collectionDetails in collectionDict:
        print(collection["name"])
        inputFile = open(
            "../hadith-api-master/editions/" + collection["name"] + ".min.json",
            # "../hadith-api/editions/ara-muslim.json",
            "r",
            encoding="utf-8",
        )
        data = json.load(inputFile)

        for hadith in data["hadiths"]:
            value = None
            if 'arabicnumber' in hadith.keys():
                value = hadith["arabicnumber"]
            gradings = ""
            for grades in hadith["grades"]:
                gradings = gradings + grades["name"] + "::" + grades["grade"] + " && "
            if(gradings.endswith(" && ")):
                gradings = gradings[:-4]
            
            cursor.execute(
                f"""INSERT INTO hadith
                (hadithnumber,arabicnumber,text,grades,bookNumber,bookhadith,bookname,language,shortname)
                VALUES(?,?,?,?,?,?,?,?,?);""",
                (
                    hadith["hadithnumber"],value,hadith["text"],gradings,hadith["reference"]["book"],hadith["reference"]["hadith"],data["metadata"]["name"],collection["language"],collectionShortNameDict[data["metadata"]["name"]]
                ),
            )
        print("complete")

            
        conn.commit()
        conn.close()
