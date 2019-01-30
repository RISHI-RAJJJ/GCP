from flask import Flask

import shutil

from google.cloud import storage
import os
import logging
import cgi, os
import cgitb; cgitb.enable()
from flask import render_template, request
app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def hii():
    return render_template("index.html")


@app.route('/upload',methods=['POST'])
def hiii():
    target=os.path.join(APP_ROOT,'files/')
    print(target)
    
    if not os.path.isdir(target):
        os.mkdir(target)
    
    for file in request.files.getlist("filename"):
        print(file)
        filename=file.filename
        destination="/".join([target,filename])
        print('destination'+destination)
        file.save(destination)
    #f = request.files['filename']
    #print(f)
    #form = cgi.FieldStorage()
    # Get filename here.
    #fileitem = form["filename"]
    #print(''+fileitem)
    
    
    # Test if the file was uploaded
   # if fileitem.filename:
    #    fn = os.path.basename(fileitem.filename)
     #   print(fn)
    #filename = secure_filename(file.filename)
    #f.save(secure_filename(f.filename))
    #file.save(os.path.join(app.config['UPLOAD_FOLDER'],f.filename))
    #fn = os.path.basename(f.filename)
    #print(fn)
        storage_client = storage.Client.from_service_account_json('C:\Users\RISHI\Videos\Mulesoft\GCP material\lively-listener-230120-9cbc1ccde30d.json')
        buckets = list(storage_client.list_buckets())
        bucket = storage_client.get_bucket("sasuke1")
        blob = bucket.blob(filename)
        blob.upload_from_filename(destination)
        
    if os.path.isdir(target):
        shutil.rmtree(target)
    return "helo world!"

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
    
    
@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
# [END app]