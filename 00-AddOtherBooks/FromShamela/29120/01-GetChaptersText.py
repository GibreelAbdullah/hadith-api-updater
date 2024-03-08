from bs4 import BeautifulSoup
getNamePagesMapping = __import__('00-GetChapterNamesAndPages')
import os

shamelaId = "29120"
arr = os.listdir('/home/alfi/Projects/hadith-supplementary/hadith/grad/{}/'.format(shamelaId))
arr.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))

chapterFolderPath = "{}/Chapters".format(shamelaId)
if not os.path.exists(chapterFolderPath):
    os.mkdir(chapterFolderPath)
fout = open("{}/Chapters/1.txt".format(shamelaId), "w")

chapterIndex = 1
for file in arr:
    f = open("/home/alfi/Projects/hadith-supplementary/hadith/grad/{}/".format(shamelaId) + file, "r")
    source_html = f.read()
    soup = BeautifulSoup(source_html, "html.parser")
    text = getattr(soup.find('div', {"class": "nass margin-top-10"}), "text", None)
    if(chapterIndex in getNamePagesMapping.getNamePagesMapping(shamelaId=shamelaId)):
        if (file.replace('.html','') == getNamePagesMapping.getNamePagesMapping(shamelaId=shamelaId).get(chapterIndex).get('startPage')):
            fout.close()
            fout = open("{}/Chapters/{}.txt".format(shamelaId, chapterIndex), "w")
            chapterIndex = chapterIndex + 1
    fout.write(text)
    f.close()
