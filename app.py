from flask import Flask, request, render_template
from azure.storage.blob import BlobServiceClient
import os

app = Flask(__name__)

CONNECTION_STRING = "PASTE_YOUR_CONNECTION_STRING"
CONTAINER_NAME = "uploads"

blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
container_client = blob_service_client.get_container_client(CONTAINER_NAME)

@app.route('/')
def home():
    return '''
    <h2>Azure File Upload</h2>
    <form method="POST" action="/upload" enctype="multipart/form-data">
        <input type="file" name="file">
        <button type="submit">Upload</button>
    </form>
    '''

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']

    blob_client = container_client.get_blob_client(file.filename)
    blob_client.upload_blob(file, overwrite=True)

    return "File uploaded successfully!"

if __name__ == '__main__':
    app.run(debug=True)