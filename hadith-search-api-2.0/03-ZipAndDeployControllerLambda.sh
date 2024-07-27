zip controller.zip controller.py

WORKER_FUNCTION_NAMES_LIST=$(ls zippedData | sed 's/\.zip$//g' | tr '\n' ',')
ROLE_ARN=$ROLE_ARN
FUNCTION_NAME="HadithSearchController"

aws lambda create-function \
    --function-name $FUNCTION_NAME \
    --runtime python3.12 \
    --role "$ROLE_ARN" \
    --handler controller.lambda_handler \
    --zip-file fileb://controller.zip \
    --environment Variables="{FUNCTION_NAME=\"${WORKER_FUNCTION_NAMES_LIST::-1}\"}" \
    --timeout 30 \
    --no-cli-pager

# aws lambda update-function-code --function-name ControllerLambda --zip-file fileb://controller.zip
# aws lambda update-function-configuration --function-name ControllerLambda --environment "Variables={FUNCTION_NAME=${FUNCTION_NAMES::-1}}"

aws lambda create-function-url-config --function-name $FUNCTION_NAME \
--auth-type NONE \
--cors AllowMethods="GET",AllowOrigins="*"