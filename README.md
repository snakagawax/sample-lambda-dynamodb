# AWS SAM DynamoDB to SNS Lambda Function

このプロジェクトは、AWS SAM を使用して DynamoDB テーブルから SNS トピックにメッセージを送信する Lambda 関数をデプロイするためのものです。

## 前提条件

- AWS CLI がインストールされていること
- AWS CLI が設定されていること (`aws configure`を実行)
- AWS SAM CLI がインストールされていること
    - 

## プロジェクトのセットアップ

### 1. リポジトリのクローン

```sh
git clone https://github.com/snakagawax/sample-lambda-dynamodb.git
cd sample-lambda-dynamodb
```

### 2. SAMテンプレートのビルド

```sh
sam build
```

### 3. SAMスタックのデプロイ

```sh
sam deploy --guided
```

プロンプトに従って、スタック名、リージョン、その他の設定を入力します。以下は例です：

```plaintext
Stack Name [sam-app]: MyDynamoDBToSNSStack
AWS Region [ap-northeast-1]: us-west-2
Confirm changes before deploy [y/N]: Y
Allow SAM CLI IAM role creation [Y/n]: Y
Disable rollback [y/N]: N
DynamoDBToSNSFunction has no authentication. Is this okay? [y/N]: Y
Save arguments to configuration file [Y/n]: Y
SAM configuration file [samconfig.toml]: samconfig.toml
SAM configuration environment [default]: default
```

## SNSサブスクリプションの追加

### 1. SNSトピックへのEmailサブスクリプション

```sh
aws sns subscribe \
    --topic-arn arn:aws:sns:ap-northeast-1:123456789012:ServiceTopicA \
    --protocol email \
    --notification-endpoint your-email@example.com

aws sns subscribe \
    --topic-arn arn:aws:sns:ap-northeast-1:123456789012:ServiceTopicB \
    --protocol email \
    --notification-endpoint your-email@example.com
```

## DynamoDBテーブルへのデータ登録

### 1. DynamoDBテーブルへのデータ登録

```sh
aws dynamodb put-item \
    --table-name ServiceTable \
    --item '{
        "serviceName": {"S": "ProjectA"},
        "snsTopicArn": {"S": "arn:aws:sns:ap-northeast-1:123456789012:ServiceTopicA"}
    }'

aws dynamodb put-item \
    --table-name ServiceTable \
    --item '{
        "serviceName": {"S": "ProjectB"},
        "snsTopicArn": {"S": "arn:aws:sns:ap-northeast-1:123456789012:ServiceTopicB"}
    }'
```

## テストの実行

### 1. テストイベントの作成

以下のような JSON 形式のテストイベントを作成します。

```json
{
    "service": "ProjectA",
    "message": "This is a test message for ProjectA"
}
```

### 2. Lambda関数のテスト実行

AWS マネジメントコンソールを使用して Lambda 関数をテストするか、AWS CLI を使用してテストを実行します。

#### AWS CLIを使用したテスト

```sh
aws lambda invoke \
    --invocation-type RequestResponse \
    --function-name sam-app-DynamoDBToSNSFunction-kXGTH4XZcnN3 \
    --region ap-northeast-1 \
    --log-type Tail \
    --payload fileb://event.json \
    response.json
```

`response.json`ファイルにレスポンスが保存されます。

## クリーンアップ

リソースを削除する場合は、以下のコマンドを実行してスタックを削除します。

```sh
sam delete --stack-name MyDynamoDBToSNSStack
```
