# READS FILES IN CHUNKS AND WHEN IT FINDS THE 

import json
import os
from unidecode import unidecode
import convert_numbers
getNamePagesMapping = __import__('00-GetChapterNamesAndPages')

hadithMap = {} # For sub-json in info.json
sectionDetails ={}

def populateHadithInfo(hadithCount, hadithCountInBook):
  hadithData = {
            "hadithnumber" : hadithCount, 
            "arabicnumber" : hadithCount, # Get a number by changing (a,b,c,d) with (.01,.02,.02,.04)
            "grades":[],
            "reference":{
                        "book": int(file.strip(".txt")),
                        "hadith": hadithCountInBook
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

bookShortName = "musnadahmad"
finalDetails = """{{
	"author": "Imam Ahmad ibn Hanbal",
	"book": "{}",
	"language": "arabic"
}}""".format(bookShortName)

shamelaId = "25794"
arr = os.listdir('{}/Chapters'.format(shamelaId))
fout = open("{}/ara-{}.txt".format(shamelaId,bookShortName), "w")

arr.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
hadithCount = 2 # When 2 is encountered, the text before it will be #1
prev_hadith = ''
current_chunk = ''

for file in arr:
  fin = open("{}/Chapters/{}".format(shamelaId,file), "r")
  hadithCountInBook = 1
  firstHadithOfBook = hadithCount - 1
  while True:  # until EOF
    chunk = fin.read(4096)  # I propose 4096 or so
    if not chunk:
      break
    current_chunk += chunk
    while(True):
      index_next_hadith = current_chunk.find(convert_numbers.english_to_hindi(hadithCount))
      if(index_next_hadith != -1):
        prev_hadith = current_chunk[:index_next_hadith]
        fout.write(str(hadithCount - 1) + ' | ' + prev_hadith + '\n')
        populateHadithInfo(hadithCount-1, hadithCountInBook)
        current_chunk = current_chunk[index_next_hadith:]
        hadithCount += 1
        hadithCountInBook += 1
        
      else:
        if(current_chunk.find(convert_numbers.english_to_hindi(hadithCount+1)) != -1):
          fout.write(str(hadithCount-1) + ' | ' + "MANUAL_CORRECTION_NEEDED" + '\n')
          populateHadithInfo(hadithCount-1, hadithCountInBook)
          hadithCount += 1
          hadithCountInBook += 1

        elif(current_chunk.find(convert_numbers.english_to_hindi(hadithCount+2)) != -1):
          fout.write(str(hadithCount-1) + ' | ' + "MANUAL_CORRECTION_NEEDED_1" + '\n')
          fout.write(str(hadithCount) + ' | ' + "MANUAL_CORRECTION_NEEDED_2" + '\n')
          populateHadithInfo(hadithCount-1, hadithCountInBook)
          populateHadithInfo(hadithCount, hadithCountInBook + 1)
          hadithCount += 2
          hadithCountInBook += 2
        break
  fout.write(str(hadithCount - 1) + ' | ' + current_chunk + '\n')
  populateHadithInfo(hadithCount-1, hadithCountInBook)
  hadithCount += 1
  hadithCountInBook += 1
  current_chunk = ''
  fin.close()
fout.writelines(finalDetails)
fout.close()

sections = {}
for chapterNumber, chapterNameAndPage in getNamePagesMapping.getNamePagesMapping(shamelaId).items():
    sections[str(chapterNumber)] = chapterNameAndPage.get("chapterName")

data = {
    bookShortName : {
        "metadata" : {
            "name": "Musnad Imam Ahmad ibn Hanbal",
            "sections": sections,
            "last_hadithnumber": hadithCount - 2,
            "section_details": sectionDetails
        },
        "hadiths": hadithMap.get(bookShortName)
    }
}
finfo = open("{}/info.json".format(shamelaId), "w")
finfo.write(json.dumps(data, indent=4 ,separators=(',', ':'), ensure_ascii=False))