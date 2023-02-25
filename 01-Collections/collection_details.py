# Generate collections.json and collections.min.json 
# List of collections in the database and the languages they are available in
import json
 
editionsFile = open('../hadith-api/editions.json','r',encoding="utf-8")
editionsData = json.load(editionsFile)

collectionDict = []
languageList = []

for collectionList, collectionListDetails in editionsData.items():
    languageList = []
    for collection in collectionListDetails["collection"]:
        languageList.append(collection["name"][:3])
    collectionDict.append(
        {"name": collectionListDetails["name"], "availableLanguages": languageList}
    )

# print(collectionDict)

editionsFile.close()

collectionsFile = open('./01-Collections/collectionList.json','r',encoding="utf-8")
collectionsData = json.load(collectionsFile)

for collection in collectionsData["collections"]:
    for collectionLanguage in collectionDict:
        if (collection["eng-name"] == collectionLanguage["name"]):
            collection["availableLanguages"] = collectionLanguage["availableLanguages"]

# print(collectionsData)

outputFile = open('../hadith-api/updates/collections/collections.json','w',encoding="utf-8")
outputFile.write(json.dumps(collectionsData, indent=4, ensure_ascii=False))

outputFile.close

outputFileMin = open('../hadith-api/updates/collections/collections.min.json','w',encoding="utf-8")
outputFileMin.write(json.dumps(collectionsData, separators=(',', ':'), ensure_ascii=False))

outputFileMin.close
