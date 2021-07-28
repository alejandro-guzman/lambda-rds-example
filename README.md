# lambda-rds-example

Reference example of AWS Lambda connecting to RDS server

## Create zip for AWS Lambda

```bash
zip -r9 function.zip . -i 'handler.py' -i 'pymysql/*' -i '*.dist-info/*'
```

## Initialize database

Run initialize script

```bash
docker run -it --rm -v $(pwd):/tmp \
    -e LAMBDA_RDS_HOSTNAME=$LAMBDA_RDS_HOSTNAME \
    -e LAMBDA_RDS_USERNAME=$LAMBDA_RDS_USERNAME \
    -e LAMBDA_RDS_PASSWORD=$LAMBDA_RDS_PASSWORD \
    mysql /bin/bash -c 'mysql --host="$LAMBDA_RDS_HOSTNAME" --user="$LAMBDA_RDS_USERNAME" --password="$LAMBDA_RDS_PASSWORD" < /tmp/db-init.sql'
```

<details>
    <summary>Direct connect with Docker</summary>

```bash
docker run -it --rm mysql mysql --host=$LAMBDA_RDS_HOSTNAME --user=$LAMBDA_RDS_USERNAME --password=$LAMBDA_RDS_PASSWORD --database=$LAMBDA_RDS_DATABASE
```
</details>

## Create AWS resources

Create AWS Lambda function

```bash
docker run --rm -it -v ~/.aws:/root/.aws -v $(pwd):/tmp amazon/aws-cli lambda --output json \
    create-function \
    --function-name LambdaRDSExampleFunction \
    --runtime python3.8 \
    --handler handler.lambda_handler \
    --description 'AWS Lambda & RDS example function' \
    --zip-file fileb:///tmp/function.zip \
    --role arn:aws:iam::380453758307:role/service-role/RDSQueryFromLambdaRole
```

Add environment variables to function

```bash
docker run --rm -v ~/.aws:/root/.aws -v $(pwd):/tmp \
    -e LAMBDA_RDS_HOSTNAME=$LAMBDA_RDS_HOSTNAME \
    -e LAMBDA_RDS_USERNAME=$LAMBDA_RDS_USERNAME \
    -e LAMBDA_RDS_PASSWORD=$LAMBDA_RDS_PASSWORD \
    -e LAMBDA_RDS_DATABASE=$LAMBDA_RDS_DATABASE \
    amazon/aws-cli lambda --output json \
    update-function-configuration \
    --function-name LambdaRDSExampleFunction \
    --environment "Variables={LAMBDA_RDS_HOSTNAME=$LAMBDA_RDS_HOSTNAME,LAMBDA_RDS_USERNAME=$LAMBDA_RDS_USERNAME,LAMBDA_RDS_PASSWORD=$LAMBDA_RDS_PASSWORD,LAMBDA_RDS_DATABASE=$LAMBDA_RDS_DATABASE}"
```

todo: 
- create role from cli
- create rds from cli
- add trigger for lambda