# # This script was supposed populate the chapter numbers which were taken from db. But becuase of certain issues in the input
# # it is not working as expected. Going for the brute force method in the next step. Hope the computer doesn't explode :D

# import sqlite3
# import json

# conn = sqlite3.connect("hadith.db")


# def getCollectionFullName(shortName):
#     mapping = {
#         "bukhari": "Sahih al Bukhari",
#         "muslim": "Sahih Muslim",
#         "nasai": "Sunan an Nasai",
#         "abudawud": "Sunan Abu Dawud",
#         "tirmidhi": "Jami At Tirmidhi",
#         "ibnmajah": "Sunan Ibn Majah",
#         "malik": "Muwatta Malik",
#     }
#     return mapping.get(shortName, " ")


# def getDBData(shortName):
#     fullName = getCollectionFullName(shortName)
#     query = '''
# 			SELECT
# 					c.title_en collection_title,
# 					h.book_id,
# 					h.order_in_book,
# 					b.title_en book_name,
# 					c2.title ara_ch_name,
# 					c2.title_en eng_ch_name,
# 					CASE
# 						h.chapter_id - h.prev_chapter_id
# 					when 0 then 0
# 						else 1
# 					end is_first_hadith_of_chapter
# 				from
# 					(
# 					SELECT
# 						h.collection_id,
# 						h.book_id,
# 						h.chapter_id,
# 						LAG ( h.chapter_id,
# 						1,
# 						0 ) OVER (
# 					ORDER BY
# 						collection_id,
# 						book_id ,
# 						order_in_book  
# 					) prev_chapter_id,
# 						h.order_in_book
# 					from
# 						hadith h
# 						) h
# 				inner  join collection c on
# 						c.id = h.collection_id
# 				left outer join book b on
# 						b.collection_id = h.collection_id
# 						and b.id = h.book_id
# 				left outer JOIN chapter c2 on
# 						c2.collection_id = h.collection_id
# 					and 
# 						c2.book_id = h.book_id
# 					and
# 						c2.id = h.chapter_id
# 				where c.title_en = "''' + fullName + '''"
# 			'''
#     cursor = conn.execute(query)
#     return cursor.fetchall()


# inputFile = open('../hadith-api/info.json', 'r', encoding="utf-8")
# data = json.load(inputFile)

# for collectionName, collectionDetails in data.items():
#     i = 0  # iterator used to iterate over data from DB
#     j = 0  # iterator used to iterate over info.json

#     prev_book = -1  # Chapter number starts from 1 in each book, when a new book comes we need to reset the chapter number to 0
#     chapterNumber = 0  # Tracks chapternumber
#     dbData = getDBData(collectionName)
    
#     # In some cases chapter names are missing (empty or null) in DB, We take the last chapter name and populate it in the current hadith
#     lastChapterNameAra = ""
#     lastChapterNameEng = ""

#     while (i < len(dbData) and j < len(data[collectionName]["hadiths"])):
#         reduceJ = 0 #reducing the indices which have been increased because the book number is not matching
#         reduceI = 0 #
#         useLastChapterFlag = False

#         if (data[collectionName]["hadiths"][j]["reference"]["book"] > dbData[i][1]):
#             i = i+1
#             reduceI = reduceI + 1
#             lastChapterNameAra = "باب"
#             lastChapterNameEng = "Chapter"
#             useLastChapterFlag = True
#         elif (data[collectionName]["hadiths"][j]["reference"]["book"] < dbData[i][1]):
#             j = j+1
#             reduceJ = reduceJ + 1
#             useLastChapterFlag = True
#         elif (data[collectionName]["hadiths"][j]["reference"]["hadith"] > dbData[i][2]):
#             i = i+1
#             reduceI = reduceI + 1
#             useLastChapterFlag = True
#         elif (data[collectionName]["hadiths"][j]["reference"]["hadith"] > dbData[i][2]):
#             j = j+1
#             reduceJ = reduceJ + 1
#             useLastChapterFlag = True
#         # if both arabic and english chapter names are empty, we will change the isFirstHadith flag to 0
#         elif (prev_book != data[collectionName]["hadiths"][j]["reference"]["book"]):
#             prev_book = data[collectionName]["hadiths"][j]["reference"]["book"]
#             chapterNumber = 0
#         elif (dbData[i][4] == dbData[i][5]):
#                 i = i+1
#                 j = j+1
#                 reduceI = reduceI + 1
#                 reduceJ = reduceJ + 1
#                 useLastChapterFlag = True
#         if (useLastChapterFlag):
#             # print(data[collectionName]["hadiths"]
#             #       [j - reduceJ]["reference"]["book"])
#             # print(data[collectionName]["hadiths"]
#             #       [j - reduceJ]["reference"]["hadith"])
#             # print(dbData[i - reduceI][2])
#             # print("\n")
#             chapterDetails = {
#                 "id": chapterNumber,
#                 "ara-name": lastChapterNameAra,
#                 "eng_name": lastChapterNameEng,
#                 "isFirstHadith": 0,
#             }
#             data[collectionName]["hadiths"][j -
#                                             reduceJ]["chapter"] = chapterDetails
#             continue
#         lastChapterNameAra = dbData[i][4]
#         lastChapterNameEng = dbData[i][5]

#         isFirstHadith = dbData[i][6]


#         # if first book of chapter, we will increase the chapter number by 1
#         if (isFirstHadith == 1):
#             chapterNumber = chapterNumber + 1

#             # if book number and hadith number in db match we will add the chapter title.
#         if (data[collectionName]["hadiths"][j]["reference"]["book"] == dbData[i][1] and data[collectionName]["hadiths"][j]["reference"]["hadith"] == dbData[i][2]):
#             chapterDetails = {
#                 "id": chapterNumber,
#                 "ara-name": dbData[i][4],
#                 "eng_name": dbData[i][5],
#                 "isFirstHadith": isFirstHadith,
#             }
#             data[collectionName]["hadiths"][j]["chapter"] = chapterDetails
#         i = i+1
#         j = j+1
# inputFile.close

# outputFile = open('../hadith-api/info_new.json', 'w', encoding="utf-8")
# outputFile.write(json.dumps(data, indent=4, ensure_ascii=False))
# outputFile.close

# # outputFileMin = open('../hadith-api/info.min.json','w',encoding="utf-8")
# # outputFileMin.write(json.dumps(data, separators=(',', ':'), ensure_ascii=False))

# # outputFileMin.close

# # print("info.json created")
