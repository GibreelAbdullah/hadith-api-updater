from bs4 import BeautifulSoup
import bs4
getNamePagesMapping = __import__('00-GetChapterNamesAndPages')
import os

shamelaId = "25794"
arr = os.listdir('/home/alfi/Projects/hadith-supplementary/hadith/grad/{}/'.format(shamelaId))
arr.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))

chapterFolderPath = "{}/Chapters".format(shamelaId)
if not os.path.exists(chapterFolderPath):
    os.mkdir(chapterFolderPath)
tafseerFolderPath = "{}/Tafseer".format(shamelaId)
if not os.path.exists(tafseerFolderPath):
    os.mkdir(tafseerFolderPath)
fout = open("{}/Chapters/1.txt".format(shamelaId), "w")
fout_tafseer = open("{}/Tafseer/1.txt".format(shamelaId), "w")

chapterIndex = 1
for file in arr:
    print(file)
    f = open("/home/alfi/Projects/hadith-supplementary/hadith/grad/{}/".format(shamelaId) + file, "r")
    source_html = f.read()
    soup = BeautifulSoup(source_html, "html.parser")
    text_all = soup.find('div', {"class": "nass margin-top-10"}).contents
    text = ""
    text_tafseer = ''
    for text_each in text_all:
        # if()
        # a = text_each.attrs
        if type(text_each) is bs4.element.Tag:
            if("hamesh" in text_each.attrs.get('class',[])):
                text_tafseer = text_tafseer + getattr(text_each, "text", None) + '، '
            else:
                text = text + getattr(text_each, "text", None) + '، '

    # Checking the first page of the next chapter. if the html file reaches that point we move to the next chapter.
    # Adding 38 because first 38 chapters are just Introductions. We have removed them from the html files as well
    if (file.replace('.html','') == getNamePagesMapping.getNamePagesMapping(shamelaId=shamelaId).get(chapterIndex+38).get('startPage')):
        fout.close()
        fout_tafseer.close()
        fout = open("{}/Chapters/{}.txt".format(shamelaId, chapterIndex), "w")
        fout_tafseer = open("{}/Tafseer/{}.txt".format(shamelaId, chapterIndex), "w")
        chapterIndex = chapterIndex + 1
    fout.write(text)
    fout_tafseer.write(text_tafseer)
    f.close()
