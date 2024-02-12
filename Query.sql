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
		h.related_hadiths
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
            50,101,102,110,113,115,130,200,300
        ) 