cd ./lambdas/controller_lambda/
zip ../../controller.zip controller.py simplify_arabic.py

cd ../../

WORKER_FUNCTION_NAMES_LIST=$(ls zippedData | sed 's/\.zip$//g' | tr '\n' ',')
FUNCTION_NAME="HadithSearchController"

if aws lambda get-function --function-name "$FUNCTION_NAME" > /dev/null 2>&1; then
    echo "Function $FUNCTION_NAME already exists. Updating it."
    aws lambda update-function-configuration \
        --function-name "$FUNCTION_NAME" \
        --environment Variables="{FUNCTION_NAME=\"${WORKER_FUNCTION_NAMES_LIST::-1}\"}" \
        --no-cli-pager
fi
