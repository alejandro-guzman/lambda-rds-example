"""
Example AWS Lambda handler.

To debug locally add function invocation:
lambda_handler(None, None)
"""
import os
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
    cursor.execute('SELECT * FROM transactions')

    rows = cursor.fetchall()
    for row in rows:
        print('{0} {1} {2}'.format(row[0], row[1], row[2]))
