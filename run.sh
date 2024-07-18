# !/bin/sh
# echo '' >> ../hadith-api/.gitignore
# echo 'editions' >> ../hadith-api/.gitignore
python3 ./01-Collections/01-CollectionDetails.py

python3 ./02-UpdateInfoJSON/01-ArabicChapterNames.py
python3 ./02-UpdateInfoJSON/02-UpdateBukhariMuslimGradings.py
python3 ./02-UpdateInfoJSON/04-AddChapterNamesBruteForce.py
python3 ./02-UpdateInfoJSON/05-AddUnmergedInfoJson.py

python3 ./03-Books/02-BookDetails2.py

cp -r 01-Collections/updates/ ../hadith-api/
