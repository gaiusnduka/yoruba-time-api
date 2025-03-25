from flask import Flask, request, jsonify
from flask_cors import CORS
import datetime
import os
import base64
from io import BytesIO
from gtts import gTTS

app = Flask(__name__)
CORS(app)

# Yoruba Numbers Dictionary
yoruba_numbers = {
    1: "kan", 2: "méjì", 3: "mẹ́ta", 4: "mẹ́rin", 5: "márùn",
    6: "mẹ́fà", 7: "méje", 8: "mẹ́jọ", 9: "mẹ́sàn", 10: "mẹ́wàá",
    11: "mókànlá", 12: "mèjìlá", 13: "mẹtàlá", 14: "mẹ́rinlá", 15: "mẹ́dọ́gún",
    16: "mẹ́rìndílógún", 17: "mẹtàdílógún", 18: "méjìdílógún", 19: "mókàndílógún", 20: "ogún",
    21: "mókanlélógún", 22: "méjìlélógún", 23: "mẹ́tàlélógún", 24: "mẹ́rinlélógún", 25: "márùnlélógún",
    26: "mẹ́fàlélógún", 27: "méjèlélógún", 28: "mẹ́jọlélógún", 29: "mẹ́sànlélógún", 30: "ààbọ̀",
    31: "mókanlélógbon", 32: "méjìlélógbon", 33: "mẹtàlélógbon", 34: "mẹ́rinlélógbon", 35: "márùnlélógbon",
    36: "mẹ́fàlélógbon", 37: "méjèlélógbon", 38: "mẹ́jọlélógbon", 39: "mẹ́sànlélógbon", 40: "ògójì",
    41: "mókànlélógójì", 42: "méjìlélógójì", 43: "mẹtàlélógójì", 44: "mẹ́rinlélógójì", 45: "mẹ́dọ́ta",
    46: "mẹ́fàlélógójì", 47: "méjèlélógójì", 48: "mẹ́jọlélógójì", 49: "mẹ́sànlélógójì", 50: "ààdọ́ta",
    51: "mókànlélààdọ́ta", 52: "méjìlélààdọ́ta", 53: "mẹtàlélààdọ́ta", 54: "mẹ́rinlélààdọ́ta", 55: "márùnlélààdọ́ta",
    56: "mẹ́fàlélààdọ́ta", 57: "méjèlélààdọ́ta", 58: "mẹ́jọlélààdọ́ta", 59: "mẹ́sànlélààdọ́ta"
}

# Yoruba Time Periods
time_periods = {
    "morning": "òwúrọ̀",  # 12:00 AM – 11:59 AM
    "afternoon": "òṣán",  # 12:00 PM – 3:59 PM
    "evening": "ìròlẹ́",  # 4:00 PM – 6:59 PM
    "night": "alẹ́",  # 7:00 PM – 11:59 PM
    "midnight": "òrù"  # 12:00 AM – 3:59 AM
}

# Function to translate time to Yoruba
def translate_time_to_yoruba(time_str):
    try:
        time_obj = datetime.datetime.strptime(time_str, "%I:%M %p")
    except ValueError:
        return "Invalid time format"

    hour = time_obj.hour
    minute = time_obj.minute

    # Convert hour (12-hour format)
    hour = 12 if hour == 0 else (hour if hour <= 12 else hour - 12)
    yoruba_hour = yoruba_numbers.get(hour, str(hour))

    # Convert minutes
    if minute == 0:
        yoruba_minute = ""
    elif minute < 30:
        yoruba_minute = f"kọjá ìṣéjú {yoruba_numbers.get(minute, minute)}"
    else:
        remaining = 60 - minute
        yoruba_hour = yoruba_numbers.get((hour % 12) + 1, str((hour % 12) + 1))
        yoruba_minute = f"ku ìṣéjú {yoruba_numbers.get(remaining, remaining)}"

    # Determine time of day
    if 0 <= time_obj.hour < 12:
        time_of_day = time_periods["morning"]
    elif 12 <= time_obj.hour < 16:
        time_of_day = time_periods["afternoon"]
    elif 16 <= time_obj.hour < 19:
        time_of_day = time_periods["evening"]
    else:
        time_of_day = time_periods["night"]

    # Construct Yoruba time translation
    yoruba_time = f"Aago {yoruba_hour} {yoruba_minute} {time_of_day}".strip()
    return yoruba_time

# API Endpoint for Translation
@app.route('/translate', methods=['POST'])
def translate():
    data = request.json
    english_time = data.get('time')

    if not english_time:
        return jsonify({"error": "Missing time input"}), 400

    yoruba_translation = translate_time_to_yoruba(english_time)
    return jsonify({"english": english_time, "yoruba": yoruba_translation})

# API Endpoint for Yoruba Text-to-Speech (TTS)
@app.route('/speak', methods=['POST'])
def speak():
    data = request.json
    yoruba_text = data.get("text")

    if not yoruba_text:
        return jsonify({"error": "Missing text input"}), 400

    try:
        tts = gTTS(yoruba_text, lang="en")
        audio_path = "yoruba_time.mp3"
        tts.save(audio_path)
        return send_file(audio_path, as_attachment=True)
    except Exception as e:
        return jsonify({"error": "Failed to generate audio", "details": str(e)}), 500

# Homepage Route
@app.route('/')
def home():
    return "Welcome to the Yoruba Time Translator API! Use /translate or /speak."

if __name__ == "__main__":
    app.run(debug=True)
