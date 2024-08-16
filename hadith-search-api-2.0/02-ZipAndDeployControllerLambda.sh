cd ./lambdas/controller_lambda/
zip ../../controller.zip controller.py simplify_arabic.py

cd ../../

WORKER_FUNCTION_NAMES_LIST=$(ls zippedData | sed 's/\.zip$//g' | tr '\n' ',')
ROLE_ARN=$ROLE_ARN
FUNCTION_NAME="HadithSearchController"

if aws lambda get-function --function-name "$FUNCTION_NAME" > /dev/null 2>&1; then
    echo "Function $FUNCTION_NAME already exists. Updating it."
    aws lambda update-function-code \
        --function-name "$FUNCTION_NAME" \
        --zip-file fileb://controller.zip \
        --no-cli-pager

else
    echo "Creating function $FUNCTION_NAME."
    aws lambda create-function \
        --function-name $FUNCTION_NAME \
        --runtime python3.12 \
        --role "$ROLE_ARN" \
        --handler controller.lambda_handler \
        --zip-file fileb://controller.zip \
        --environment Variables="{FUNCTION_NAME=\"${WORKER_FUNCTION_NAMES_LIST::-1}\"}" \
        --timeout 30 \
        --no-cli-pager
    aws lambda create-function-url-config --function-name $FUNCTION_NAME \
    --auth-type NONE \
    --cors AllowMethods="GET",AllowOrigins="*"
fi
