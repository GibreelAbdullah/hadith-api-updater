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

from lambdas.controller_lambda.simplify_arabic import simplify_arabic_text

hadith_worker_prefix = 'hadith_search_worker_'

def get_connection(hadithShardNumber):
    path = "data/" + hadith_worker_prefix + str(hadithShardNumber)
    if not os.path.exists(path):
        os.makedirs(path)
    if os.path.exists(path + "/hadith.db"):
        os.remove(path + "/hadith.db")
    conn = sqlite3.connect(path + "/hadith.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS hadith;")
    cursor.execute("CREATE VIRTUAL TABLE IF NOT EXISTS hadith USING FTS5(hadithnumber,arabicnumber,text,grades,bookNumber,bookhadith,bookname,language,shortname, tokenize = 'unicode61 remove_diacritics 1');")

    return conn, cursor

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

hadithShardNumber = 1
conn, cursor = get_connection(hadithShardNumber)
hadith_map ={}
collection_names = []
for collectionList, collectionListDetails in sorted(editionsData.items()):
    for collection in collectionListDetails["collection"]:
        if(collection["name"].startswith("ara-") and collection["name"].endswith("1")):
            continue
        collection_names.append(collection["name"])

collection_names = sorted(collection_names)
for collection in collection_names:
    # for collectionDetails in collectionDict:
    print(collection)
    inputFile = open(
        "../hadith-api-master/editions/" + collection + ".min.json",
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
        
        if(collection.startswith("ara-")):
            hadith_text = simplify_arabic_text(hadith["text"])
        else:
            hadith_text = hadith["text"]

        cursor.execute(
            f"""INSERT INTO hadith
            (hadithnumber,arabicnumber,text,grades,bookNumber,bookhadith,bookname,language,shortname)
            VALUES(?,?,?,?,?,?,?,?,?);""",
            (
                hadith["hadithnumber"],value,hadith_text,gradings,hadith["reference"]["book"],hadith["reference"]["hadith"],data["metadata"]["name"],collection[:3],collectionShortNameDict[data["metadata"]["name"]]
            ),
        )
    if hadith_worker_prefix + str(hadithShardNumber) not in hadith_map:
        hadith_map[hadith_worker_prefix + str(hadithShardNumber)] = [collection]
    else:
        hadith_map[hadith_worker_prefix + str(hadithShardNumber)].append(collection)
        
    print("complete")
        
    conn.commit()
    
    database_size = os.path.getsize(f"data/{hadith_worker_prefix}{hadithShardNumber}/hadith.db")
    if database_size > 150*1024*1024:
        conn.close()
        hadithShardNumber += 1
        conn, cursor = get_connection(hadithShardNumber)

# print(hadith_map)
with open('./lambdas/controller_lambda/hadith_map.json', 'w') as outfile:
    json.dump(hadith_map, outfile)
