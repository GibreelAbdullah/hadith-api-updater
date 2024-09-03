
import json
import os


def remove_duplicates(lst):
    return [dict(t) for t in {tuple(d.items()) for d in lst}]


def update_info(gradings_map):
    filepath = "./hadith-api/info.json"

    with open(filepath, 'r', encoding='utf8') as f:
        data = json.load(f)
        f.close()
    
    for subjson in gradings_map:
        collection = subjson['collection']
        hadithNumber = subjson['hadithNumber']
        grades = subjson['grades']

        for i, hadith in enumerate(data[collection]['hadiths']):
            if int(hadith['hadithnumber']) == hadithNumber:
                grades.extend(data[collection]['hadiths'][i]['grades'])

                data[collection]['hadiths'][i]['grades'] = remove_duplicates(
                    grades + subjson['grades'])
          
    with open(filepath, 'w', encoding='utf8') as f:
        json.dump(data, f, indent=4)
        f.close()


if __name__ == "__main__":
    gradings_map = [
        {
            "collection": "ibnmajah",
            "hadithNumber": 1129,
            "grades": [
                {
                    "name": "Abu Zur'ah al-Iraqi",
                    "grade": "Isnaad Jayyid",
                    "source": "طرح التثریب: ۳/۴۱، ط:المصریة القدیمة"
                },
                {
                    "name": "Zain al-Din al-Iraqi",
                    "grade": "Isnaad Jayyid",
                    "source": "فیض القدیر شرح جامع الصغیر (۵/۲۱۶، ط: التجاریة)"
                },
            ],
        },
        {
            "collection": "tirmidhi",
            "hadithNumber": 257,
            "grades": [
                {
                    "name": "Imam Tirmidhi",
                    "grade": "Hasan",
                },
                {
                    "name": "Darqutni",
                    "grade": "Isnaad Sahih",
                    "source": "کتاب العلل الدارقطنی ج 5 ص 172 سوال 804 (https://shamela.ws/book/9082/1503)"
                },
                {
                    "name": "Ibn Hazm",
                    "grade": "Sahih",
                    "source": "كتاب المحلى بالآثار ج 2 ص 578 (https://shamela.ws/book/767/808)"
                },
                {
                    "name": "Ibn Al-Qataan Al-Faasi",
                    "grade": "Close to Sahih",
                    "source": "بيان الوهم والإيهام في كتاب الأحكام (https://shamela.ws/book/5923/946#p1)"
                },
                {
                    "name": "Jamal Al-Din Al-Zylaeei",
                    "grade": "Sahih",
                    "source": "كتاب نصب الراية ج 1 ص 396 (shamela.ws/book/11428/431)"
                },
                {
                    "name": "Badr al-Din al-Ayni",
                    "grade": "Sahih",
                    "source": "كتاب شرح سنن أبي داود للعيني ج 2 ص 346 (https://shamela.ws/book/8540/1348#p1"
                },
                {
                    "name": "Anwar Shah Kashmiri",
                    "grade": "Sahih",
                    "source": "نيل الفرقدين في مسألة رفع اليدين ص 56"
                }
            ],
        },
    ]

    # collection = "ibnmajah"
    # hadithNumber = 1129
    # grades = [{
    #     "name": "Abu Zur'ah al-Iraqi",
    #     "grade": "Isnaad Jayyid",
    #     "source": "طرح التثریب: ۳/۴۱، ط:المصریة القدیمة"
    # },
    #     {
    #     "name": "Zain al-Din al-Iraqi",
    #     "grade": "Isnaad Jayyid",
    #     "source": "فیض القدیر شرح جامع الصغیر (۵/۲۱۶، ط: التجاریة)"
    # },]
    update_info(gradings_map)
