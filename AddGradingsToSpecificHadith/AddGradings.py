
import json
import os


def remove_duplicates(lst):
    return [dict(t) for t in {tuple(d.items()) for d in lst}]


def update_info(collection, hadithNumber, grades):
    filepath = "./hadith-api/info.json"

    with open(filepath, 'r') as f:
        data = json.load(f)
        f.close()
    for i, hadith in enumerate(data[collection]['hadiths']):
        if int(hadith['hadithnumber']) == hadithNumber:
            grades.extend(data[collection]['hadiths'][i]['grades'])

            data[collection]['hadiths'][i]['grades'] = remove_duplicates(
                grades)

    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)
        f.close()


if __name__ == "__main__":
    collection = "ibnmajah"
    hadithNumber = 1129
    grades = [{
        "name": "Abu Zur'ah al-Iraqi",
        "grade": "Isnaad Jayyid",
        "source": "طرح التثریب: ۳/۴۱، ط:المصریة القدیمة"
    },
        {
        "name": "Zain al-Din al-Iraqi",
        "grade": "Isnaad Jayyid",
        "source": "فیض القدیر شرح جامع الصغیر (۵/۲۱۶، ط: التجاریة)"
    }]
    update_info(collection, hadithNumber, grades)
