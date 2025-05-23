from flask import Flask, jsonify, send_from_directory
from api import fetch_and_convert
import os

app = Flask(__name__)

@app.route('/get-audio-data', methods=['GET'])
def get_audio_data():
    results = fetch_and_convert()
    return jsonify(results)

@app.route('/audios/<filename>')
def serve_audio(filename):
    # Serve audio files from the 'converted_audios' folder
    return send_from_directory('converted_audios', filename)

if __name__ == "__main__":
    # Ensure the directory exists
    if not os.path.exists('converted_audios'):
        os.makedirs('converted_audios')
    
    app.run(host='0.0.0.0', port=5000, debug=True)
