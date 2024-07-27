# import json

# inputFile = open('./hadith-api/info.json','r+',encoding="utf-8")
# data = json.load(inputFile)

# for collectionName, collectionDetails in data.items():
#     for hadithList in data[collectionName]["hadiths"]:
#         newgrade = []
#         for grades in hadithList["grades"]:
#             if (grades["name"] != "Zubair Ali Zai"):
#                 newgrade.append({
#                     "name": grades["name"],
# 					"grade": grades["grade"]
#                 })
#         hadithList["grades"] = newgrade
                
# inputFile.seek(0) # rewind
# inputFile.write(json.dumps(data, indent=4, ensure_ascii=False))
# inputFile.truncate()

# inputFile.close
