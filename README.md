# lambda-rds-example

Reference example of AWS Lambda connecting to RDS server

## Ordered Steps

- [x] .env
- [x] function.zip
- [ ] rds server
- [ ] rds init
- [ ] lambda role
- [x] lambda func
- [x] lambda env
- [ ] lambda trigger

## 1. Create `.env`

```bash
$ cat << EOF > .env
export LAMBDA_RDS_USERNAME=admin
export LAMBDA_RDS_PASSWORD=s3cr3ts3cr3t
export LAMBDA_RDS_DATABASE=demodb1
export LAMBDA_RDS_DB_INSTANCE_ID=demodbinstance
EOF
$ source .env
```

<details>
    <summary>Create a secure password!</summary>

```bash
head -c 16 /dev/urandom | base64 | tr -dc A-Za-z0-9; echo
```
</details>

## 2. Create AWS RDS instance

```bash
docker run --rm -v ~/.aws:/root/.aws amazon/aws-cli rds --output json \
    create-db-instance \
    --db-instance-identifier $LAMBDA_RDS_DB_INSTANCE_ID \
    --db-name $LAMBDA_RDS_DATABASE \
    --db-instance-class db.t2.micro \
    --engine mysql \
    --allocated-storage 20 \
    --master-username $LAMBDA_RDS_USERNAME \
    --master-user-password $LAMBDA_RDS_PASSWORD \
    --publicly-accessible
```

<details>
    <summary>To delete AWS RDS resource</summary>
   
```bash
docker run --rm -v ~/.aws:/root/.aws amazon/aws-cli rds --output json \
    delete-db-instance --db-instance-identifier $LAMBDA_RDS_DB_INSTANCE_ID --skip-final-snapshot
```
</details>

## 3. Get RDS hostname

```bash
docker run --rm -v ~/.aws:/root/.aws amazon/aws-cli rds --output json \
    describe-db-instances --db-instance-identifier $LAMBDA_RDS_DB_INSTANCE_ID \
    | jq -r .DBInstances[0].Endpoint.Address
```

## 4. Add RDS hostname to `.env`

```bash
$ cat << EOF >> .env
export LAMBDA_RDS_HOSTNAME=demodbinstance.xxxxxxxxxxxx.region.rds.amazonaws.com
EOF
$ source .env
```

## 5. Initialize database

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

## 6. Create zip for AWS Lambda

```bash
zip -r9 function.zip . -i 'handler.py' -i 'pymysql/*' -i '*.dist-info/*'
```

## Create AWS resources

Create AWS Lambda function

```bash
docker run --rm -v ~/.aws:/root/.aws -v $(pwd):/tmp amazon/aws-cli lambda --output json \
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
docker run --rm -v ~/.aws:/root/.aws amazon/aws-cli lambda --output json \
    update-function-configuration \
    --function-name LambdaRDSExampleFunction \
    --environment "Variables={LAMBDA_RDS_HOSTNAME=$LAMBDA_RDS_HOSTNAME,LAMBDA_RDS_USERNAME=$LAMBDA_RDS_USERNAME,LAMBDA_RDS_PASSWORD=$LAMBDA_RDS_PASSWORD,LAMBDA_RDS_DATABASE=$LAMBDA_RDS_DATABASE}"
```

todo: 
- create role from cli
- ~~create rds from cli~~
- add trigger for lambda
- organize the docs better