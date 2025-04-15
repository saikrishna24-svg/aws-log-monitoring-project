import boto3
import gzip
import json
import base64

dynamodb = boto3.resource('dynamodb')
sns = boto3.client('sns')

table = dynamodb.Table('LogTable')
sns_topic_arn = 'arn:aws:sns:us-east-1:982081073833:log-alert-topic'  # replace with your ARN

def lambda_handler(event, context):
    # Step 1: Decode and unzip
    compressed_payload = base64.b64decode(event['awslogs']['data'])
    uncompressed_payload = gzip.decompress(compressed_payload)
    payload = json.loads(uncompressed_payload)

    # Step 2: Iterate through log events
    for log_event in payload['logEvents']:
        log_message = log_event['message']
        parts = log_message.split(" - ")
        
        if len(parts) != 3:
            print("Invalid log format:", log_message)
            continue
        
        log_time, log_level, log_text = parts

        # Step 3: Store to DynamoDB
        table.put_item(
            Item={
                'log_id': log_event['id'],
                'timestamp': log_time,
                'level': log_level,
                'message': log_text
            }
        )

        # Step 4: Trigger SNS if error
        if log_level.strip().upper() == "ERROR":
            sns.publish(
                TopicArn=sns_topic_arn,
                Subject="🚨 Error Log Detected!",
                Message=f"[{log_time}] {log_text}"
            )

    return {"status": "done"}
