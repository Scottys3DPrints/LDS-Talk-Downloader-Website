from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess

app = Flask(__name__)
CORS(app)

# Paths to your Python scripts
GC_DOWNLOAD_PATH = "C:\\Users\\samuh\\OneDrive\\Dokumente\\Scotty's Documents\\_Programming\\vscode_samuel_programming\\LDS Talk Downloader Website\\Python\\GC_downloads.py"
BYU_DOWNLOAD_PATH = "C:\\Users\\samuh\\OneDrive\\Dokumente\\Scotty's Documents\\_Programming\\vscode_samuel_programming\\LDS Talk Downloader Website\\Python\\BYU_downloads.py"
GC_BYU_DOWNLOAD_PATH = "C:\\Users\\samuh\\OneDrive\\Dokumente\\Scotty's Documents\\_Programming\\vscode_samuel_programming\\LDS Talk Downloader Website\\Python\\GC+BYU_download.py"

# Route to run GC_downloads.py
@app.route('/gc_download', methods=['POST'])
def gc_download():
    data = request.get_json()
    name = data.get('name')
    if not name:
        return jsonify({"error": "No name provided"}), 400

    print(f"Running GC_downloads.py for: {name}")
    try:
        subprocess.run(["python", GC_DOWNLOAD_PATH], check=True)
        return jsonify({"message": f"GC downloads triggered for {name}"}), 200
    except Exception as e:
        print(f"Error running GC_downloads.py: {e}")
        return jsonify({"error": str(e)}), 500

# Route to run BYU_downloads.py
@app.route('/byu_download', methods=['POST'])
def byu_download():
    data = request.get_json()
    name = data.get('name')
    if not name:
        return jsonify({"error": "No name provided"}), 400

    print(f"Running BYU_downloads.py for: {name}")
    try:
        subprocess.run(["python", BYU_DOWNLOAD_PATH], check=True)
        return jsonify({"message": f"BYU downloads triggered for {name}"}), 200
    except Exception as e:
        print(f"Error running BYU_downloads.py: {e}")
        return jsonify({"error": str(e)}), 500

# Route to run GC+BYU_download.py
@app.route('/gc_byu_download', methods=['POST'])
def gc_byu_download():
    data = request.get_json()
    name = data.get('name')
    if not name:
        return jsonify({"error": "No name provided"}), 400

    print(f"Running GC+BYU_download.py for: {name}")
    try:
        subprocess.run(["python", GC_BYU_DOWNLOAD_PATH], check=True)
        return jsonify({"message": f"GC + BYU downloads triggered for {name}"}), 200
    except Exception as e:
        print(f"Error running GC+BYU_download.py: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
