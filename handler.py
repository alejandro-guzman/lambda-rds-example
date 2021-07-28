"""
Example AWS Lambda handler.

Requires pymysql bundles with handler:
`python3 -m pip install -t $(pwd) pymysql`

To debug locally add function invocation:
lambda_handler(None, None)
"""
import os
import json
import pymysql

hostname = os.getenv('LAMBDA_RDS_HOSTNAME')
username = os.getenv('LAMBDA_RDS_USERNAME')
password = os.getenv('LAMBDA_RDS_PASSWORD')
database = os.getenv('LAMBDA_RDS_DATABASE')

connection = pymysql.connect(host=hostname, user=username,
    password=password, database=database)

def lambda_handler(event, context):
    """Example AWS Lambda hander"""

    # debug event and context
    print('event', event)
    print('context', context)

    cursor = connection.cursor()
    cursor.execute('SELECT first_name, company_name \
        FROM user u JOIN company c ON u.company_id = c.company_id')

    rows = cursor.fetchall()
    for row in rows:
        res = {'first_name': row[0], 'company_name': row[1]}
        print(json.dumps(res))
