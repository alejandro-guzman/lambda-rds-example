import pymysql
from os import getenv

hostname = getenv('LAMBDA_RDS_HOSTNAME')
username = getenv('LAMBDA_RDS_USERNAME')
password = getenv('LAMBDA_RDS_PASSWORD')
database = getenv('LAMBDA_RDS_DATABASE')

connection = pymysql.connect(host=hostname, user=username,
    password=password, database=database)

def lambda_handler(event, context):
    # debug event and context
    print('event', event)
    print('context', context)

    cursor = connection.cursor()
    cursor.execute('SELECT * FROM transactions')

    rows = cursor.fetchall()
    for row in rows:
        print('{0} {1} {2}'.format(row[0], row[1], row[2]))
