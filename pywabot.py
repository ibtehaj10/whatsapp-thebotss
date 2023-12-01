from pywa import WhatsApp
from flask import Flask
from pywa.types import Message, CallbackButton
from pywa import filters
import requests
import json
import speech_recognition as sr
from pydub import AudioSegment


flask_app = Flask(__name__)

def stt(filename):


    # Initialize recognizer
    recognizer = sr.Recognizer()

    # Load your audio file
    audio_file_path = filename  # replace with your file path

    # Use the audio file as the source
    with sr.AudioFile(audio_file_path) as source:
        # Record the audio file
        audio_data = recognizer.record(source)

        # Recognize the content
        try:
            # Recognize speech using Google Web Speech API
            text = recognizer.recognize_google(audio_data, language='ur-PK')  # Urdu - Pakistan
            print("Recognized text:", text)
            return text
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")






def convert_to_wav(audio_file_path):
    # Load the audio file
    audio = AudioSegment.from_file(audio_file_path)

    # Define the output file name
    output_file_path = audio_file_path.split('.')[0] + '.wav'

    # Export the file as WAV
    audio.export(output_file_path, format="wav")
    print('audio export done')
    return output_file_path







def gpt(user_id,prompt):


    url = "http://10.41.0.75:5002/chat"

    payload = json.dumps({
    "prompt": prompt,
    "user_id": user_id
    })
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    res = response.json()
    return res['message']['content']




wa = WhatsApp(
    phone_id='113578631653943',
    token='EAAMTxi1SmKQBO4jVUEwiLJihCocbxPGbMeuBWOonBQeJA03DWvDNxrVRACSoOzrGEudZAQvhJ78rMBaZAGPxZCtIzSuW4JUAZCyM9lqfMhhyUNbtcZB7vivyVBdLxzP4ZBgUexOJiYaAfW5Nl3GkPlTjoAkcQhh5jEielBKESGEXmEg422bwjvFmgxzROfqHe2afW7WXRFk7IPMS3S76gZD',
    server=flask_app,
    callback_url='https://8736-212-129-37-129.ngrok-free.app',
    verify_token='asd',
    app_id=866166814972068,
    app_secret='522cb40c7b628187a09133bf8e1ab931'
)

@wa.on_message()
def audio(client: WhatsApp, msg: Message):
    uid = msg.from_user.wa_id
    types = msg.type
    
    print('type : ',type)
    
    if types == 'audio':
    # if msg.audio:
        audio = msg.audio
        audio_name = msg.download_media('audios/')
        wav = convert_to_wav(audio_name)
        txt = stt(wav)
        reply = gpt(uid,txt)
        print(reply)
        msg.reply_text(
            text=reply
        )
    elif types == 'text':
        print("we got text input")
        print('msg : ',msgs)
        msgs = msg.text
        reply = gpt(uid,msgs)
        msg.reply_text(
            text=reply
        )
    else:
        print(types)









flask_app.run()  # Run the flask app to start the server