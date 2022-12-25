# # PENDING , first run ../02-UpdateInfoJSON/02-FixReferences.py


# import json
 
# inputFile = open('../info_test.json','r',encoding="utf-8")
# data = json.load(inputFile)

# collection = {}
# collectionList = []

# currentBook = ''
# for collectionName, collectionDetails in data.items():
#     minHadith = 0
#     maxHadith = 0
#     book = -1
#     for hadith in collectionDetails["hadiths"]:
#         if(hadith["reference"]["book"] == book):
#             minHadith = min(minHadith,hadith["hadithnumber"])
#             maxHadith = max(maxHadith,hadith["hadithnumber"])
#         else:
#             if(book==-1):
#                 "skip"
#             if(collectionName == 'muslim'):
#                print("CollectionName = "+ collectionName+ "  & Book = ", book, "  &  From ", minHadith, " To ", maxHadith)
#             book = hadith["reference"]["book"]
#             minHadith = hadith["hadithnumber"]
#             maxHadith = hadith["hadithnumber"]
#     print("CollectionName = "+ collectionName+ "  & Book = ", book, "  &  From ", minHadith, " To ", maxHadith)



# # collectionList = sorted(collectionList, key=lambda d: d['order']) 

# # outputFile = open('collections.json','w',encoding="utf-8")
# # outputFileMin = open('collections.min.json','w',encoding="utf-8")

# # outputFile.write(json.dumps({"collections":collectionList}, indent=4, ensure_ascii=False))
# # outputFileMin.write(json.dumps({"collections":collectionList},separators=(',', ':'), ensure_ascii=False))

# # print("collections.json and collections.min.json created")

# # inputFile.close
# # outputFile.close
# # outputFileMin.close