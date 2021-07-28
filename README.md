# lambda-rds-example

Reference example of AWS Lambda connecting to RDS server

## Create zip for AWS Lambda

```bash
zip -r9 function.zip . -i 'handler.py' -i 'pymysql/*' -i '*.dist-info/*'
```

## Initialize database

Run initialize script

```bash
docker run -it --rm \
    -e LAMBDA_RDS_HOSTNAME=$LAMBDA_RDS_HOSTNAME \
    -e LAMBDA_RDS_USERNAME=$LAMBDA_RDS_USERNAME \
    -e LAMBDA_RDS_PASSWORD=$LAMBDA_RDS_PASSWORD \
    -v $PWD:/tmp \
    mysql /bin/bash -c 'mysql --host="$LAMBDA_RDS_HOSTNAME" --user="$LAMBDA_RDS_USERNAME" --password="$LAMBDA_RDS_PASSWORD" < /tmp/db-init.sql'
```

<details>
    <summary>Direct connect with Docker</summary>

```bash
docker run -it --rm mysql mysql --host=$LAMBDA_RDS_HOSTNAME --user=$LAMBDA_RDS_USERNAME --password=$LAMBDA_RDS_PASSWORD --database=$LAMBDA_RDS_DATABASE
```
</details>
