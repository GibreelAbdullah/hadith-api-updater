#!/bin/bash

# Enable exit on error
set -e

# Function to run Python script and check its exit status
# Function to run a command and check its exit status
run_command() {
    echo "Running: $@"
    "$@"
    local status=$?
    if [ $status -ne 0 ]; then
        echo "Error: Command '$@' failed with exit status $status"
        exit $status
    fi
}


run_command python3 ./01-Collections/01-CollectionDetails.py

run_command python3 ./02-UpdateInfoJSON/01-ArabicChapterNames.py
run_command python3 ./02-UpdateInfoJSON/02-UpdateBukhariMuslimGradings.py
run_command python3 ./02-UpdateInfoJSON/04-AddChapterNamesBruteForce.py
run_command python3 ./02-UpdateInfoJSON/05-AddUnmergedInfoJson.py
run_command python3 ./03-Books/02-BookDetails2.py
run_command python3 ./AddGradingsToSpecificHadith/AddGradings.py

run_command cd ./hadith-api
run_command npm install
run_command npx playwright install
run_command export CI=true
run_command node apiscript.js update
run_command cp -r ../02-UpdateInfoJSON/hadithTexts/* ./start/
run_command node apiscript.js create
run_command cd ..
run_command rm -rf ./hadith-api-master/editions/
run_command cp -r ./hadith-api/editions/ ./hadith-api-master/ && cd ./hadith-api-master && find ./editions/ -type f ! \( -name "*.min.json" -o -name "*.html" \) -delete

echo "All scripts completed successfully"