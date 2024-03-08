# Get the starting page of each chapter. This is needed to segregate each hadith into chapters

from bs4 import BeautifulSoup

def is_int(s):
    try: 
        int(s)
    except ValueError:
        return False
    else:
        return True


def getNamePagesMapping(shamelaId):
    f = open("../hadith/grad/book-{}.html".format(shamelaId), "r")
    source_html = f.read()
    soup = BeautifulSoup(source_html, "html.parser")
    namePagesMapping = {}
    file_number = 1
    chapter_number = 1
    old_start_page = 0
    for link in soup.find('div', {"class": "betaka-index"}).find_all('a'):
        start_page = link.attrs.get('href').replace('https://shamela.ws/book/{}/'.format(shamelaId),'')
        if(is_int(start_page)): # Some cases the chapter has a parent chapter as well and startPage is not there, we only need the immediate chapter name
            if(int(start_page) > 152): # The starting intro chapters are to be skipped
                if(old_start_page != start_page):
                    namePagesMapping[chapter_number] = {
                        "chapterName" : link.string,
                        "startPage" : start_page
                    }
                    chapter_number = chapter_number + 1
                else:
                    namePagesMapping[chapter_number - 1] = {
                        "chapterName" : link.string,
                        "startPage" : start_page
                    }
                old_start_page = start_page
        file_number = file_number + 1
    f.close()
    return(namePagesMapping)

if __name__ == "__main__":
    print(getNamePagesMapping("25794"))