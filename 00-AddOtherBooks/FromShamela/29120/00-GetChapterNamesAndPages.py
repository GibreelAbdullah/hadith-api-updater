# Get the starting page of each chapter. This is needed to segregate each hadith into chapters

from bs4 import BeautifulSoup

def getNamePagesMapping(shamelaId):
    f = open("../hadith/grad/book-{}.html".format(shamelaId), "r")
    source_html = f.read()
    soup = BeautifulSoup(source_html, "html.parser")
    namePagesMapping = {}
    i = 1
    for link in soup.find('div', {"class": "betaka-index"}).find_all('a'):
        namePagesMapping[i] = {
            "chapterName" : link.string,
            "startPage" : link.attrs.get('href').replace('https://shamela.ws/book/{}/'.format(shamelaId),'')
        }
        i = i + 1
    f.close()
    return(namePagesMapping)

if __name__ == "__main__":
    print(getNamePagesMapping("29120"))