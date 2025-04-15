# Grant CloudWatch Logs permission to invoke Lambda function
aws lambda add-permission \
  --function-name <YourLambdaFunctionName> \
  --statement-id  AllowCWLogsInvoke\
  --action "lambda:InvokeFunction" \
  --principal logs.amazonaws.com \
  --source-arn arn:aws:logs:<YourRegion>:<YourAWSAccountID>:log-group:<YourLogGroupName>:* \
  --region <YourRegion>
  
# Create a CloudWatch Logs Subscription Filter to forward logs to Lambda
aws logs put-subscription-filter \
  --log-group-name <YourLogGroupName> \
  --filter-name <YourFilterName> \  
  --filter-pattern "" \  # Empty pattern means all logs are forwarded
  --destination-arn arn:aws:lambda:<YourRegion>:<YourAWSAccountID>:function:<YourLambdaFunctionName> 

# Send a test log event to CloudWatch Logs
aws logs put-log-events \
  --log-group-name <YourLogGroupName> \ 
  --log-stream-name <YourLogStreamName> \ 
  --log-events timestamp=$(date +%s%3N),message="<YourLogMessage>" \ 
  --sequence-token <YourSequenceToken>  # Replace with the sequence token from the previous log 

