##PENDING ON https://github.com/fawazahmed0/hadith-api/issues/23

import json

inputFile = open('../info.json','r',encoding="utf-8")
data = json.load(inputFile)

def formatNumber(num):
  if num % 1 == 0:
    return int(num)
  else:
    return num

for collectionName, collectionDetails in data.items():
    precedingReference = 0
    currentReference = 0
    nextReference = 0
    for index, hadith in enumerate(collectionDetails["hadiths"]):
        if (index == 0):
            continue
        else:
            precedingReference = collectionDetails["hadiths"][index - 1]["reference"]
            currentReference = collectionDetails["hadiths"][index]["reference"]
            try:
                nextReference = collectionDetails["hadiths"][index + 1]["reference"]
            except:
                continue
        if(currentReference["book"] == 0 and precedingReference["book"] == nextReference["book"] and precedingReference["book"]!= currentReference["book"] and precedingReference["book"] != 0):
            currentReference["book"] = precedingReference["book"]
            currentReference["hadith"] = formatNumber((precedingReference["hadith"]+nextReference["hadith"])/2)
            collectionDetails["hadiths"][index]["reference"] = currentReference

outputFile = open('../info_test.json','w',encoding="utf-8")
outputFile.write(json.dumps(data, indent=4, ensure_ascii=False))

inputFile.close
outputFile.close

# print("info_new.json created")
