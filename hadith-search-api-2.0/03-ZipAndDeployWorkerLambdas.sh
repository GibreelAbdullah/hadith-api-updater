WORKER_LAMBDA_DIR="./lambdas/worker_lambda"

for dir in data/*; do
    if [ -d "$dir" ]; then
        subfolder=$(basename "$dir")
        (
            cd "$dir"
            zip -r "../../zippedData/${subfolder}.zip" hadith.db
            cd "../../$WORKER_LAMBDA_DIR"
            zip -r "../../zippedData/${subfolder}.zip" "app.py" "query.py"
        )
    fi
done

#!/bin/bash

# IAM role ARN for Lambda functions
ROLE_ARN=$ROLE_ARN

# Loop through each zip file in the zippedData directory
for zip_file in zippedData/*.zip; do
    # Extract the base name of the zip file (without directory path)
    base_name=$(basename "$zip_file")

    # Remove the .zip extension to get the function name
    function_name="${base_name%.zip}"


    # Check if the function already exists (ignore error if it doesn't)
    if aws lambda get-function --function-name "$function_name" > /dev/null 2>&1; then
        echo "Function $function_name already exists. Updating it."
        echo "Size of $zip_file: $(du -sh "$zip_file" | cut -f1)"
        aws lambda update-function-code \
            --function-name "$function_name" \
            --zip-file fileb://"$zip_file" \
            --no-cli-pager
    else
        echo "Creating function $function_name."
        echo "Size of $zip_file: $(du -sh "$zip_file" | cut -f1)"
        aws lambda create-function \
            --function-name "$function_name" \
            --runtime python3.12 \
            --role "$ROLE_ARN" \
            --handler app.lambda_handler \
            --zip-file fileb://"$zip_file" \
            --timeout 30 \
            --no-cli-pager

    fi
done
