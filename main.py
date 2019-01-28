from flask import Flask

from google.cloud import storage
import os
import logging

app = Flask(__name__)




@app.route('/')
def hello():
    storage_client = storage.Client.from_service_account_json('C:\Users\RISHI\Videos\Mulesoft\GCP material\My Project 69244-55dbb853fec6.json')
    buckets = list(storage_client.list_buckets())
    bucket = storage_client.get_bucket("sasuke")
    blob = bucket.blob("C:\Users\RISHI\Videos\Mulesoft\GCP material\GCP1.txt")

    blob.upload_from_filename("C:\Users\RISHI\Videos\Mulesoft\GCP material\GCP1.txt")

    print(buckets)
    return "helo world!"


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)









@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
# [END app]