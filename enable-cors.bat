aws apigateway update-integration-response ^
  --rest-api-id c1nl0knyal ^
  --resource-id RESOURCE_ID ^
  --http-method ANY ^
  --status-code 200 ^
  --patch-operations op=add,path=/responseParameters/method.response.header.Access-Control-Allow-Origin,value="'*'"

aws apigateway put-method-response ^
  --rest-api-id c1nl0knyal ^
  --resource-id RESOURCE_ID ^
  --http-method OPTIONS ^
  --status-code 200 ^
  --response-parameters method.response.header.Access-Control-Allow-Headers=true,method.response.header.Access-Control-Allow-Methods=true,method.response.header.Access-Control-Allow-Origin=true

aws apigateway put-integration ^
  --rest-api-id c1nl0knyal ^
  --resource-id RESOURCE_ID ^
  --http-method OPTIONS ^
  --type MOCK ^
  --request-templates "{\"application/json\":\"{\\\"statusCode\\\": 200}\"}"

aws apigateway put-integration-response ^
  --rest-api-id c1nl0knyal ^
  --resource-id RESOURCE_ID ^
  --http-method OPTIONS ^
  --status-code 200 ^
  --response-parameters method.response.header.Access-Control-Allow-Headers="'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'",method.response.header.Access-Control-Allow-Methods="'GET,PUT,POST,DELETE,HEAD,OPTIONS'",method.response.header.Access-Control-Allow-Origin="'*'"

aws apigateway create-deployment --rest-api-id c1nl0knyal --stage-name dev
