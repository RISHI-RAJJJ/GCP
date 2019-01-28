import datetime
import logging
import os

from flask import Flask, render_template, request, Response
import sqlalchemy


# Remember - storing secrets in plaintext is potentially unsafe. Consider using
# something like https://cloud.google.com/kms/ to help keep secrets secret.
db_user = os.environ.get("DB_USER")
db_pass = os.environ.get("DB_PASS")
db_name = os.environ.get("DB_NAME")
cloud_sql_instance_name = os.environ.get("CLOUD_SQL_INSTANCE_NAME")

app = Flask(__name__)

logger = logging.getLogger()

# [START cloud_sql_mysql_connection_pool]
# The SQLAlchemy engine will help manage interactions, including automatically
# managing a pool of connections to your database
db = sqlalchemy.create_engine(
    # Equivalent URL:
    # mysql+pymysql://<db_user>:<db_pass>@/<db_name>?unix_socket=/cloudsql/<cloud_sql_instance_name>
    sqlalchemy.engine.url.URL(
        drivername='mysql+pymysql',
        username=db_user,
        password=db_pass,
        database=db_name,
        query={
            'unix_socket': '/cloudsql/{}'.format(cloud_sql_instance_name)
        }
    ),
    # ... Specify additional properties here.
    # [START_EXCLUDE]

    # [START cloud_sql_mysql_limit_connections]
    # Pool size is the maximum number of permanent connections to keep.
   # pool_size=5,
    # Temporarily exceeds the set pool_size if no connections are available.
 #   max_overflow=2,
    # The total number of concurrent connections for your application will be
    # a total of pool_size and max_overflow.
    # [END cloud_sql_mysql_limit_connections]

    # [START cloud_sql_mysql_connection_backoff]
    # SQLAlchemy automatically uses delays between failed connection attempts,
    # but provides no arguments for configuration.
    # [END cloud_sql_mysql_connection_backoff]

    # [START cloud_sql_mysql_connection_timeout]
    # 'pool_timeout' is the maximum number of seconds to wait when retrieving a
    # new connection from the pool. After the specified amount of time, an
    # exception will be thrown.
 #   pool_timeout=30,  # 30 seconds
    # [END cloud_sql_mysql_connection_timeout]

    # [START cloud_sql_mysql_connection_lifetime]
    # 'pool_recycle' is the maximum number of seconds a connection can persist.
    # Connections that live longer than the specified amount of time will be
    # reestablished
  #  pool_recycle=1800,  # 30 minutes
    # [END cloud_sql_mysql_connection_lifetime]

    # [END_EXCLUDE]
)

@app.route('/')
def hello():
    
    cursor = db.connect()
    cursor.execute('SELECT * FROM table1')
    ans= cursor.fetchall()  

    for i in ans: 
        print(i) 
    return 'Hello World!'

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)

@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
# [END app]