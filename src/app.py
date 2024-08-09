import json
import boto3
import os
import logging

dynamodb = boto3.client('dynamodb')
sns = boto3.client('sns')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    # 環境変数の検証
    table_name = os.environ.get('TABLE_NAME')
    if not table_name:
        raise Exception("TABLE_NAME environment variable is not set")

    # 入力データの検証
    body = json.loads(event['body'])
    if 'service' not in body or 'message' not in body:
        raise Exception("Event object must contain 'service' and 'message' keys")

    service_name = body['service']
    message = body['message']

    # DynamoDBからSNSトピックARNを取得
    try:
        response = dynamodb.get_item(
            TableName=table_name,
            Key={
                'serviceName': {'S': service_name}
            }
        )
    except Exception as e:
        logger.error(f"Error fetching item from DynamoDB: {str(e)}")
        raise Exception(f"Error fetching item from DynamoDB: {str(e)}")

    if 'Item' not in response:
        raise Exception(f"SNS Topic ARN not found for service: {service_name}")

    sns_topic_arn = response['Item']['snsTopicArn']['S']

    # SNSトピックにメッセージを送信
    try:
        sns.publish(
            TopicArn=sns_topic_arn,
            Message=message
        )
    except Exception as e:
        logger.error(f"Error publishing message to SNS: {str(e)}")
        raise Exception(f"Error publishing message to SNS: {str(e)}")

    return {
        'statusCode': 200,
        'body': 'Message sent to SNS topic'
    }