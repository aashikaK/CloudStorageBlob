from flask import Flask, request, redirect
from azure.storage.blob import BlobServiceClient
import os

app = Flask(__name__)

# 🔴 Paste your Azure connection string here
CONNECTION_STRING = os.getenv("AZURE_CONNECTION_STRING")

CONTAINER_NAME = "uploads"

blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
container_client = blob_service_client.get_container_client(CONTAINER_NAME)


# ---------------- HOME PAGE ----------------
@app.route('/')
def home():

    blobs = container_client.list_blobs()

    file_list = ""
    for blob in blobs:
        file_list += f"""
        <div style="display:flex;justify-content:space-between;
                    padding:10px;border:1px solid #ddd;
                    margin-top:10px;border-radius:8px;">
            <span>📄 {blob.name}</span>
            <div>
                <a href="/download/{blob.name}">⬇ Download</a> |
                <a href="/delete/{blob.name}">🗑 Delete</a>
            </div>
        </div>
        """

    return f"""
<!DOCTYPE html>
<html>
<head>
    <title>Cloud Drive</title>
    <style>
        body {{
            font-family: Arial;
            background: #f5f5f5;
            display: flex;
            justify-content: center;
        }}

        .box {{
            width: 500px;
            background: white;
            padding: 25px;
            margin-top: 50px;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }}

        h2 {{
            color: #4285F4;
            text-align: center;
        }}

        .upload {{
            border: 2px dashed #ccc;
            padding: 20px;
            text-align: center;
            border-radius: 10px;
        }}

        .btn {{
            background: #4285F4;
            color: white;
            padding: 8px 15px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            margin-top: 10px;
        }}

        a {{
            text-decoration: none;
            color: #4285F4;
        }}
    </style>
</head>

<body>

<div class="box">

    <h2>My Cloud Drive</h2>

    <form method="POST" action="/upload" enctype="multipart/form-data">
        <div class="upload">
            <p>Upload File</p>
            <input type="file" name="file">
            <br>
            <button class="btn" type="submit">Upload</button>
        </div>
    </form>

    <h3 style="margin-top:20px;">Files</h3>
    {file_list}

</div>

</body>
</html>
"""


# ---------------- UPLOAD ----------------
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']

    blob_client = container_client.get_blob_client(file.filename)
    blob_client.upload_blob(file, overwrite=True)

    return redirect('/')


# ---------------- DOWNLOAD ----------------
@app.route('/download/<filename>')
def download(filename):
    blob_client = container_client.get_blob_client(filename)

    stream = blob_client.download_blob().readall()

    return (
        stream,
        200,
        {
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )


# ---------------- DELETE ----------------
@app.route('/delete/<filename>')
def delete(filename):
    blob_client = container_client.get_blob_client(filename)
    blob_client.delete_blob()
    return redirect('/')


# ---------------- RUN APP ----------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)




    # host='0.0.0.0'