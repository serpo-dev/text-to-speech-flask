import asyncio
from flask import Flask, jsonify, request, send_file, after_this_request
from speech import get_speech_file_name
import os

APP = Flask(__name__)
LOOP = asyncio.get_event_loop()

@APP.route("/", methods=["POST"])
def generate_speech_file():
    try:
        data = request.json
        text = data["text"]
        file_name = LOOP.run_until_complete(get_speech_file_name(text))
        return send_file(file_name + ".wav", mimetype="audio/wav")
    except Exception as e:
        message = {"message": str(e)}
        return jsonify(message), 404
    
    
   


if __name__ == "__main__":
    APP.run()