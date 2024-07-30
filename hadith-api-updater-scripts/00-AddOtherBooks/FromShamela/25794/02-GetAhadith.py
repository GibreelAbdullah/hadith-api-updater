# # READS HADITH CHAPTER AND PARTITIONS BASED ON REGEX. THIS IS PROVING DIFFICULT. SEE 02-GetAhadithNew.py

# import json
# import re
# import os
# from unidecode import unidecode
# import convert_numbers
# getNamePagesMapping = __import__('00-GetChapterNamesAndPages')


# def getHadithAndNumberInBook(hadith):
#     strippedHadith = re.sub(r"^[ ]*[٠-٩]+ -[ ]*","",hadith)
#     hadithNumberInBook = unidecode(re.findall(r"^[ ]*[٠-٩]+", hadith)[0])
#     return {"hadith":strippedHadith, "hadithNumberInBook" : hadithNumberInBook}


# data = {} # For info.json
# hadithMap = {} # For sub-json in info.json
# sectionDetails ={}

# bookShortName = "musnadahmad_number"
# finalDetails = """{{
# 	"author": "Imam Ahmad ibn Hanbal",
# 	"book": "{}",
# 	"language": "arabic"
# }}""".format(bookShortName)

# shamelaId = "25794"
# arr = os.listdir('{}/Chapters'.format(shamelaId))
# fout = open("{}/ara-{}.txt".format(shamelaId,bookShortName), "w")

# arr.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
# hadithCount = 1
# for file in arr:
#     fin = open("{}/Chapters/{}".format(shamelaId,file), "r")
#     map = {}

#     text = fin.read()
#     hadithList = re.findall(r"[/٠-٩]+ -.+?(?=[/٠-٩]+ -|$)", text) #Regex pattern to match "[٠-٩]+ -" followed by any character until the same pattern "[٠-٩]+ -" is seen or end of line is reached
    
#     firstHadithOfBook = hadithCount
#     prev_hadith_number = ''
#     prev_hadith = ''

#     for hadith in hadithList:
#         # Writing Hadith
#         hadithAndNumberInBookMap = getHadithAndNumberInBook(hadith)
#         if(int(hadithAndNumberInBookMap.get("hadithNumberInBook")) < int(hadithCount)):
#             prev_hadith_number = prev_hadith_number + hadithAndNumberInBookMap.get("hadithNumberInBook") + ' '
#             prev_hadith = prev_hadith + hadithAndNumberInBookMap.get("hadith") + ' '
#             continue


#         # if(hadithCount == 11782):
#         #     print("")
#         combined_hadith:str = prev_hadith + hadithAndNumberInBookMap.get("hadith")

#         if(convert_numbers.english_to_hindi(str(hadithCount-1)) in combined_hadith):
#             print("")

#         fout.write(str(hadithCount) + ' | ' + combined_hadith + '\n')
#         if(hadithCount != int(hadithAndNumberInBookMap.get("hadithNumberInBook"))):
#             arabic_number = convert_numbers.english_to_hindi(hadithCount)
#             if(arabic_number in combined_hadith):
#                 split_hadith = combined_hadith.split(arabic_number)
#             else:    
#                 print(convert_numbers.english_to_hindi(hadithCount))
#                 print(hadithCount)
#         prev_hadith_number = ''
#         prev_hadith = ''
#         # Writing Info 
#         hadithData = {
#             "hadithnumber" : hadithCount, 
#             "arabicnumber" : hadithCount, # Get a number by changing (a,b,c,d) with (.01,.02,.02,.04)
#             "grades":[],
#             "reference":{
#                         "book": int(file.strip(".txt")),
#                         "hadith": int(hadithAndNumberInBookMap.get("hadithNumberInBook"))
#                     }
#         }
#         if(bookShortName) in hadithMap:
#             hadithMap[bookShortName].append(hadithData)
#         else:
#             hadithMap[bookShortName] = [hadithData]

#         hadithCount = hadithCount + 1
#     sectionDetails[file.strip(".txt")] = {
#         "hadithnumber_first": firstHadithOfBook,
#         "hadithnumber_last": hadithCount - 1,
#         "arabicnumber_first": firstHadithOfBook,
#         "arabicnumber_last": hadithCount - 1
#     }

#     fin.close()

# fout.writelines(finalDetails)

# fout.close()

# sections = {}
# for chapterNumber, chapterNameAndPage in getNamePagesMapping.getNamePagesMapping(shamelaId).items():
#     sections[str(chapterNumber)] = chapterNameAndPage.get("chapterName")


# data = {
#     bookShortName : {
#         "metadata" : {
#             "name": "Musnad Imam Abu Hanifa",
#             "sections": sections,
#             "last_hadithnumber": hadithCount - 1,
#             "section_details": sectionDetails
#         },
#         "hadiths": hadithMap.get(bookShortName)
#     }
# }


# finfo = open("{}/info.json".format(shamelaId), "w")
# finfo.write(json.dumps(data, indent=4 ,separators=(',', ':'), ensure_ascii=False))

    