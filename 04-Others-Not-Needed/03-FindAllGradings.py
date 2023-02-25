
import json

inputFile = open('../hadith-api/info.json','r',encoding="utf-8")
data = json.load(inputFile)

gradeset = set(())

for collectionName, collectionDetails in data.items():
    sectionList = {}
    for hadithList in data[collectionName]["hadiths"]:
        for hadithGradings in hadithList["grades"]:
            gradeset.add(hadithGradings["grade"])

print(gradeset)
inputFile.close