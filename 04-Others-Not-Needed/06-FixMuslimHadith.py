import os
import re

missingHadithList = []
with open('./04-Others-Not-Needed/MissingMuslimHadith.txt', 'r') as f:
    for count, line in enumerate(f, start=1):
        if count % 2 == 0:
            missingHadithList.append(line.split('|'))


path = "/home/alfi/Projects/hadith-api-updater/TempOutput/"
dir_list = os.listdir(path)

matchingCollections = list(filter(lambda string: "muslim" in string, dir_list))
print(matchingCollections)
for collection in matchingCollections:
    print(collection)
    inputFile = open(path + collection, 'r+', encoding="utf-8")
    lines = inputFile.readlines()
    for line in lines:
        for missingHadith in missingHadithList:
            sameHadithFlag = False
            for i in range(int(missingHadith[0])-1):
                if (line.startswith(missingHadith[1].strip() + ' |')):
                    inputFile.writelines(str(int(missingHadith[1])+i+1) + ' |' + line.split('|')[1])
                i = i + 1
    inputFile.close
