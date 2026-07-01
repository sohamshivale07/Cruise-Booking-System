from flask import Flask, send_from_directory
import os

app = Flask(__name__, static_folder='.')

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('.', path)

if __name__ == '__main__':
    print("Starting frontend server on http://127.0.0.1:3000")
    print("Make sure to also run 'python app.py' for the API server on port 5000")
    app.run(port=3000, debug=True)