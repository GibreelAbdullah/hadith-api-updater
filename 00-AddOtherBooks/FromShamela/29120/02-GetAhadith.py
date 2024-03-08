import json
import re
import os
from unidecode import unidecode
getNamePagesMapping = __import__('00-GetChapterNamesAndPages')


def getHadithAndNumberInBook(hadith):
    strippedHadith = re.sub(r"^[ ]*[٠-٩]+ -[ ]*","",hadith)
    hadithNumberInBook = unidecode(re.findall(r"^[ ]*[٠-٩]+", hadith)[0])
    return {"hadith":strippedHadith, "hadithNumberInBook" : hadithNumberInBook}


data = {} # For info.json
hadithMap = {} # For sub-json in info.json
sectionDetails ={}

bookShortName = "abuhanifa"
finalDetails = """{{
	"author": "Imam Abu Hanifa",
	"book": "{}",
	"language": "arabic"
}}""".format(bookShortName)

shamelaId = "29120"
arr = os.listdir('{}/Chapters'.format(shamelaId))
fout = open("{}/ara-{}.txt".format(shamelaId,bookShortName), "w")

arr.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
hadithCount = 1
for file in arr:
    fin = open("{}/Chapters/{}".format(shamelaId,file), "r")
    map = {}

    text = fin.read()
    hadithList = re.findall(r"[٠-٩]+ -.+?(?=[٠-٩]+ -|$)", text) #Regex pattern to match "[٠-٩]+ -" followed by any character until the same pattern "[٠-٩]+ -" is seen or end of line is reached
    
    firstHadithOfBook = hadithCount

    for hadith in hadithList:
        # Writing Hadith
        hadithAndNumberInBookMap = getHadithAndNumberInBook(hadith)
        fout.write(str(hadithCount) + ' | ' + hadithAndNumberInBookMap.get("hadith") + '\n')

        # Writing Info 
        hadithData = {
            "hadithnumber" : hadithCount, 
            "arabicnumber" : hadithCount, # Get a number by changing (a,b,c,d) with (.01,.02,.02,.04)
            "grades":[],
            "reference":{
                        "book": int(file.strip(".txt")),
                        "hadith": int(hadithAndNumberInBookMap.get("hadithNumberInBook"))
                    }
        }
        if(bookShortName) in hadithMap:
            hadithMap[bookShortName].append(hadithData)
        else:
            hadithMap[bookShortName] = [hadithData]

        hadithCount = hadithCount + 1
    sectionDetails[file.strip(".txt")] = {
        "hadithnumber_first": firstHadithOfBook,
        "hadithnumber_last": hadithCount - 1,
        "arabicnumber_first": firstHadithOfBook,
        "arabicnumber_last": hadithCount - 1
    }

    fin.close()

fout.writelines(finalDetails)

fout.close()

sections = {}
for chapterNumber, chapterNameAndPage in getNamePagesMapping.getNamePagesMapping(shamelaId).items():
    sections[str(chapterNumber)] = chapterNameAndPage.get("chapterName")


data = {
    bookShortName : {
        "metadata" : {
            "name": "Musnad Imam Abu Hanifa",
            "sections": sections,
            "last_hadithnumber": hadithCount - 1,
            "section_details": sectionDetails
        },
        "hadiths": hadithMap.get(bookShortName)
    }
}


finfo = open("{}/info.json".format(shamelaId), "w")
finfo.write(json.dumps(data, indent=4 ,separators=(',', ':'), ensure_ascii=False))

    