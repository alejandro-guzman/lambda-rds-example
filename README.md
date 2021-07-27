# lambda-rds-example

Reference example of AWS Lambda connecting to RDS server

## Create zip for AWS Lambda

```bash
zip -r9 function.zip . -i 'handler.py' -i 'pymysql/*' -i '*.dist-info/*'
```

