# WARNING - RUN ONLY ONCE, IF RAN TWICE THE SECTIONS JSON WILL BECOME EMPTY SINCE ORIGINAL FILE IS BEING MODIFIED
import json
from ChapterNamesMapping import chapter_names_mapping

mapping = {
    "bukhari" : "Sahih al Bukhari",
    "muslim" : "Sahih Muslim",
    "nasai" : "Sunan an Nasai",
    "abudawud" : "Sunan Abu Dawud",
    "tirmidhi" : "Jami At Tirmidhi",
    "ibnmajah" : "Sunan Ibn Majah",
    "malik" : "Muwatta Malik",
    "abuhanifa" : "Musnad Imam Abu Hanifa"
}

inputFile = open('./hadith-api/info.json','r+',encoding="utf-8")
input_data = json.load(inputFile)

#  Current Format
            # "sections": {
			# 	"0": "",
			# 	"1": "Forty Hadith of Shah Waliullah Dehlawi"
			# },
#  Required Format
            # "sections": {
            #     "0": {
            #         "eng-name": "",
            #         "ara-name": ""
            #       }
            # }
sectionList = {}

for input_collection_name, input_collection_details in input_data.items():
    for input_section_id, input_section_name in input_collection_details["metadata"]["sections"].items():
        if (chapter_names_mapping.get(mapping.get(input_collection_name,""),"") == ""):
            input_collection_details["metadata"]["sections"][input_section_id] = {"eng-name": input_section_name, "ara-name": ""}
        else:
            input_collection_details["metadata"]["sections"][input_section_id] = {"eng-name": input_section_name, "ara-name": chapter_names_mapping.get(mapping.get(input_collection_name,"")).get(input_section_name, "")}
# for collection_name_full, chapter_name_map in chapter_names_mapping.items():
#     if(input_data.get(mapping.get(collection_name_full,""),"") == ""):
#        continue
#     for sectionId, sectionName in input_data[mapping.get(collection_name_full,"")]["metadata"]["sections"].items():
#       input_data[mapping.get(collection_name_full,"")]["metadata"]["sections"][sectionId] = {"eng-name": sectionName,
#                      "ara-name": chapter_name_map.get(sectionName, "")}
      
inputFile.seek(0)
inputFile.write(json.dumps(input_data, indent=4, ensure_ascii=False))
inputFile.truncate()
inputFile.close


outputFileMin = open('./hadith-api/info.min.json','w',encoding="utf-8")
outputFileMin.write(json.dumps(input_data, separators=(',', ':'), ensure_ascii=False))

outputFileMin.close

print("info.json created")
