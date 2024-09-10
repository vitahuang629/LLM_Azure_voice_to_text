#clean environment
from IPython import get_ipython
get_ipython().magic('reset -f')
import json  
import os
import azure.cognitiveservices.speech as speechsdk
import time

speech_key = "speech_key"
service_region = "eastasia"
audio_file = "20240219_03-26-09_6281398084010.wav"   

speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region, speech_recognition_language = "zh-TW" )
#speech_config.speech_recognition_language = "zh-TW"
audio_config = speechsdk.audio.AudioConfig(filename=audio_file)
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

output_file_path = "output_311.txt"

def on_recognized(evt):
    result = evt.result
    print(result.text)
    with open(output_file_path, "a", encoding="utf-8") as file:
        file.write(result.text + "\n")

def on_session_stopped(evt):
    print('SESSION STOPPED {}'.format(evt))
    global done
    done = True

speech_recognizer.recognized.connect(on_recognized)
speech_recognizer.session_stopped.connect(on_session_stopped)

done = False
speech_recognizer.start_continuous_recognition()

while not done:
    time.sleep(1)

speech_recognizer.stop_continuous_recognition()

'''
multiple voice recognition
'''
import os
import time
import azure.cognitiveservices.speech as speechsdk
output_file_path = "output.txt"
speech_key = "speech_key"
service_region = "eastasia"
audio_file = "17.wav"

def conversation_transcriber_recognition_canceled_cb(evt: speechsdk.SessionEventArgs):
    print('Canceled event')

def conversation_transcriber_session_stopped_cb(evt: speechsdk.SessionEventArgs):
    print('SessionStopped event')

def conversation_transcriber_transcribed_cb(evt: speechsdk.SpeechRecognitionEventArgs):
    print('TRANSCRIBED:')
    if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print('\tText={}'.format(evt.result.text))
        print('\tSpeaker ID={}'.format(evt.result.speaker_id))
        with open(output_file_path, "a", encoding="utf-8") as file:
            file.write(evt.result.speaker_id +':' + evt.result.text + "\n")
    elif evt.result.reason == speechsdk.ResultReason.NoMatch:
        print('\tNOMATCH: Speech could not be TRANSCRIBED: {}'.format(evt.result.no_match_details))

def conversation_transcriber_session_started_cb(evt: speechsdk.SessionEventArgs):
    print('SessionStarted event')

def recognize_from_file():
    # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region, speech_recognition_language = "zh-TW" )
    audio_config = speechsdk.audio.AudioConfig(filename=audio_file)
    conversation_transcriber = speechsdk.transcription.ConversationTranscriber(speech_config=speech_config, audio_config=audio_config)

    transcribing_stop = False

    def stop_cb(evt: speechsdk.SessionEventArgs):
        #"""callback that signals to stop continuous recognition upon receiving an event `evt`"""
        print('CLOSING on {}'.format(evt))
        nonlocal transcribing_stop
        transcribing_stop = True

    # Connect callbacks to the events fired by the conversation transcriber
    conversation_transcriber.transcribed.connect(conversation_transcriber_transcribed_cb)
    conversation_transcriber.session_started.connect(conversation_transcriber_session_started_cb)
    conversation_transcriber.session_stopped.connect(conversation_transcriber_session_stopped_cb)
    conversation_transcriber.canceled.connect(conversation_transcriber_recognition_canceled_cb)
    # stop transcribing on either session stopped or canceled events
    conversation_transcriber.session_stopped.connect(stop_cb)
    conversation_transcriber.canceled.connect(stop_cb)

    conversation_transcriber.start_transcribing_async()

    # Waits for completion.
    while not transcribing_stop:
        time.sleep(.5)
    conversation_transcriber.stop_transcribing_async()

# Main
try:
    recognize_from_file()
except Exception as err:
    print("Encountered exception. {}".format(err))
    

# =============================================================================
# import opensmile
# 
# smile = opensmile.Smile(
#     feature_set=opensmile.FeatureSet.ComParE_2016,
#     feature_level=opensmile.FeatureLevel.Functionals,
# )
# y = smile.process_file('17.wav')
# =============================================================================
