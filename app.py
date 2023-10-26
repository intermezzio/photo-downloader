from flask import Flask, render_template, request, jsonify, send_file
import os
import shutil
import zipfile
import socket
import pyqrcode

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'

@app.route('/', methods=['GET'])
def main_page():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    uploaded_filenames = []

    for i in range(len(request.files.getlist('file'))):
        uploaded_file = request.files.getlist('file')[i]

        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
        shutil.copyfileobj(uploaded_file.stream, open(file_path, 'wb'))
        
        uploaded_filenames.append(file_path)

    return jsonify({"uploaded_files": uploaded_filenames})

def get_ip():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.settimeout(0)
            s.connect(('10.254.254.254', 1))
            ip_addr = s.getsockname()[0]
    except:
        ip_addr = "127.0.0.1"
    return ip_addr

if __name__ == '__main__':
    local_addr = get_ip()
    port = 8080
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    url = f"http://{local_addr}:{port}"
    text = pyqrcode.create(url)
    
    print(text.terminal(module_color='reverse', background='default', quiet_zone=1))
    print("Scan this link for the webpage or for automatic downloading via iOS Shortcuts\n\n")

    app.run(host=local_addr, port=port)
