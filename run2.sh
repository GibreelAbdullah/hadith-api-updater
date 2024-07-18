cd ../hadith-api
cp -r ./database/linebyline/* ./start
export CI=true
node apiscript.js update

rm -r ../hadith-api-master/updates/ && rm -r ../hadith-api-master/editions/ && cp -r ../hadith-api/updates/ ../hadith-api-master/ && cp -r ../hadith-api/editions/ ../hadith-api-master/ && cd ../hadith-api-master && find ./editions/ -type f ! \( -name "*.min.json" -o -name "*.html" \) -delete
git add . && git commit -m "Added Arabic Musnad Imam Abu Hanifa And Musnad Imam Ahmad" && git push