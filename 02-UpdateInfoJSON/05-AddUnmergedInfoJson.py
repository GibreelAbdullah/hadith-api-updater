import json
import os

inputFile = open('../hadith-api/info.json', 'r+', encoding="utf-8")
data:dict = json.load(inputFile)

infoFiles = os.listdir('./02-UpdateInfoJSON/InfoJsons')
for file in infoFiles:
    with open(os.path.join('./02-UpdateInfoJSON/InfoJsons', file), 'r', encoding="utf-8") as infoFile:
        infoData = json.load(infoFile)
        data.update(infoData)
        infoFile.close()

inputFile.seek(0)
inputFile.write(json.dumps(data, indent=4, ensure_ascii=False))
inputFile.truncate()
inputFile.close
