# from bs4 import BeautifulSoup
# import os

# shamelaId = "29120"
# arr = os.listdir('/home/alfi/Projects/hadith-supplementary/hadith/grad/{}/'.format(shamelaId))
# arr.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))

# fout = open("Scripts/ShamelaScrapForText/{}/FullText.txt".format(shamelaId), "w")

# for file in arr:
#     f = open("./grad/{}/".format(shamelaId) + file, "r")
#     source_html = f.read()
#     soup = BeautifulSoup(source_html, "html.parser")
#     fout.write(getattr(soup.find('div', {"class": "nass margin-top-10"}), "text", None))
#     f.close()
