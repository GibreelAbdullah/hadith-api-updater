# Change the h.collection_id for books and hadith table only contains arabic hadith, for english hadith use hadith_en table.
query = '''
    select
        c.title collection_name_ara,
        c.title_en collection_name,
        b.display_number book_number,
        b.title book_name_ara,
        b.title_en book_name_eng,
        b.hadith_start hadith_start_in_book,
        b.hadith_end hadith_end_in_book,
		ch.id chapter_id,
		h.narrator_prefix,
		h.content,
		h.narrator_postfix,
		h.display_number,
		h.order_in_book,
		h.narrators,
		h.related_hadiths,
		'ara' language
    from
        hadith h 
	left outer join
		collection c 
			on c.id = h.collection_id
    left outer join
        book b 
            on b.collection_id = h.collection_id
			and b.id = h.book_id
    left outer join
        chapter ch 
            on ch.collection_id = h.collection_id
			and ch.book_id = h.book_id
			and ch.id = h.chapter_id
    where
        h.collection_id in (
            50
        ) '''
#  , 110,113, 115, 130, 200, 300
def getCollectionShortName(fullName):
    mapping = {
        "Forty Hadith of an-Nawawi" : "nawawi",
        "Forty Hadith Qudsi" : "qudsi",
        "Forty Hadith of Shah Waliullah Dehlawi" : "dehlawi",
        "Musnad Ahmad" : "musnad",
        "Riyad as-Salihin" : "riyad",
        "Mishkat al-Masabih" : "mishkat",
        "Al-Adab Al-Mufrad" : "adab",
        "Ash-Shama'il Al-Muhammadiyah" : "shamail",
        "Bulugh al-Maram" : "maram",
        "Hisn al-Muslim" : "hisn"
    }
    return mapping.get(fullName, " ")

def getArabicNumberWithNumerals(hadithnumber):
    return formatNumber(float(hadithnumber.replace('a','.01').replace('b','.02').replace('c','.03').replace('d','.04').replace('e','.05')))


def formatNumber(num):
  if num % 1 == 0:
    return int(num)
  else:
    return num