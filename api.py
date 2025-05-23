import requests
from pydub import AudioSegment
from io import BytesIO
import os

SAVE_DIR = "converted_audios"
os.makedirs(SAVE_DIR, exist_ok=True)

# Apna public base URL yahan daalo — ye tumhara ngrok ya deployed server ka URL hona chahiye
BASE_URL = "https://d42a-2409-40e3-1012-9611-8d7f-7073-2505-d3f4.ngrok-free.app"

def download_audio(url):
    response = requests.get(url)
    if response.status_code == 200:
        return BytesIO(response.content)
    return None

def convert_to_mp3(audio_bytes, original_format):
    audio = AudioSegment.from_file(audio_bytes, format=original_format)
    mp3_io = BytesIO()
    audio.export(mp3_io, format="mp3")
    mp3_io.seek(0)
    return mp3_io

def fetch_and_convert(api_url="https://sample.xtrascale.com/api.php"):
    response = requests.get(api_url)
    if response.status_code != 200:
        raise Exception(f"API request failed with status {response.status_code}")

    data = response.json().get('data', [])
    results = []

    for item in data:
        uid = item['uid']
        awb = item['awb']
        audio_url = item['audio_url']

        audio_bytes = download_audio(audio_url)
        if audio_bytes is None:
            print(f"Failed to download audio for UID: {uid}")
            continue

        original_format = audio_url.split('.')[-1].lower()
        if original_format not in ['wav', 'mp3', 'ogg', 'flac', 'aac', 'm4a']:
            original_format = 'wav'

        try:
            mp3_audio = convert_to_mp3(audio_bytes, original_format)
        except Exception as e:
            print(f"Conversion failed for UID: {uid}, Error: {e}")
            continue

        mp3_filename = f"{awb}.mp3"
        mp3_filepath = os.path.join(SAVE_DIR, mp3_filename)

        with open(mp3_filepath, "wb") as f:
            f.write(mp3_audio.read())

        # Public URL of the converted mp3 file
        mp3_url = f"{BASE_URL}/audios/{mp3_filename}"

        results.append({
            "uid": uid,
            "awb": awb,
            "mp3_url": mp3_url
        })

    return results
