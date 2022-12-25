import json

inputFile = open('../../hadith-api/info.json','r+',encoding="utf-8")
data = json.load(inputFile)

for collectionName, collectionDetails in data.items():
    if(collectionName == "bukhari"):
        for hadithList in data[collectionName]["hadiths"]:
            if (hadithList["grades"] == []):
                hadithList["grades"].append({
						"name": "Imam Bukhari",
						"grade": "Sahih"
					})
    elif(collectionName == "muslim"):
        for hadithList in data[collectionName]["hadiths"]:
            if (hadithList["grades"] == [] and hadithList["hadithnumber"]>92):
                hadithList["grades"].append({
						"name": "Imam Muslim",
						"grade": "Sahih"
					})
inputFile.seek(0) # rewind
inputFile.write(json.dumps(data, indent=4, ensure_ascii=False))

inputFile.close
