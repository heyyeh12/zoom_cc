import json
import requests
import speech_recognition as sr
import sys
from distutils.util import strtobool

"""Simple application using SpeechRecognition to provide Zoom closed captions.

NOTE: This module requires some dependencies
To install using pip:

    pip install speechrecognization
    pip install requests

Example usage:
    python speech_recognizer_closed_captions.py
"""

sys.stdout.write('\033[K')
GREEN = '\u001b[32m'
YELLOW = '\u001b[33m'
RESET = '\u001b[0m'

class ZoomClosedCaptions:
    """
    Provides closed captions with SpeechRecognition libary via Zoom 3rd party clsoed caption API
    """

    def __init__(self):
        """
        Initialization
        """
        self.r = sr.Recognizer()
        # self.r.non_speaking_duration 
        # self.r.phrase_threshold
        # self.r.operation_timeout
        self.mic = sr.Microphone()
        self.seq_count = 0
        self.post_params = {'seq': str(self.seq_count), 'lang': 'en-US'}
        self.payload = ''
        self.mic_timeout = 3

        if strtobool(input("Load settings from config?")):
            self.load_config()
        else:
            self.set_Zoom_API_token()
        
        self.run()

    def __exit__(self, exception_type, exception_value, traceback):
        print('in __exit__')
        self.save_config()

    def set_Zoom_API_token(self):
        """
        Configure Zoom API settings
        """
        # Command line input
        API_ENDPOINT = str(input(YELLOW+'Enter the API token from Zoom > Closed Caption > Use a 3rd party CC service:\n>>'+RESET))
        while not API_ENDPOINT or "http" not in API_ENDPOINT:
            API_ENDPOINT = str(input('>>'))

        i = input(YELLOW+'Enter start sequence number:\n>>'+RESET)
        if not i:
            print('Using 0 by default')
            i = 0
        else:
            try:
                i = int(i)
            except ValueError:
                print('Invalid number, using 0 by default')
                i = 0
        self.api_token = API_ENDPOINT
        self.seq_count = i
    
    def load_config(self):
        """
        Load Zoom API settings from file
        """
        with open('settings.json') as config_file:
            data = json.load(config_file)
        
        # Required parameters
        self.api_token = data['zoom_api_token']
        self.seq_count = data['seq_count']
        if not self.api_token:
            print("Missing API token from settings")
            self.api_token = str(input(YELLOW+'Enter the API token from Zoom > Closed Caption > Use a 3rd party CC service:\n>>'+RESET))
            while not self.api_token or "http" not in self.api_token:
                self.api_token = str(input('>>'))
            self.seq_count = 0

        # Optinal parameters
        if 'mic_timeout' in data:
            self.mic_timeout = int(data['mic_timeout'])
        if 'lang' in data and data['lang']:
            self.post_params['lang'] = data['lang']
        
    def save_config(self):
        """
        Save settings on exit
        """
        print('Updating settings.json')
        with open('settings.json') as config_file:
            data = json.load(config_file)
        data['zoom_api_token'] = self.api_token
        data['seq_count'] = self.seq_count
        with open('settings.json', 'w') as outfile:
            json.dump(data, outfile, indent=4)

    def run(self):
        """
        Run speech recognition / POST loop
        """
        while True:
            try:
                with self.mic as source:
                    print('Calibrating for ambient noise...')
                    self.r.adjust_for_ambient_noise(source)
                    print('Energy threshold={}'.format(self.r.energy_threshold))
                    print(YELLOW+'Say something (or press ctrl+C to exit)'+RESET)
                    try:
                        audio = self.r.listen(source, timeout=self.mic_timeout)
                        print('Transcribing...')
                        self.payload = self.r.recognize_google(audio)
                        #self.payload = r.recognize_sphinx(audio)
                    except KeyboardInterrupt:
                        print("{}Exiting. Last sequence sent = {} {}".format(YELLOW, self.seq_count, RESET))
                        break
                    except sr.WaitTimeoutError:
                        print("Timeout error, continuing...")
                        continue
                    except sr.UnknownValueError:
                        print("Unknown value error, continuing...")
                        continue
                    except:
                        print("{}Unexpected error: {}{}".format(RED, sys.exc_info()[0], RESET))
                        raise
                
                print("{} >> seq {}: {} {}".format(GREEN, self.seq_count, self.payload, RESET))
                self.post_params['seq'] = str(self.seq_count)
                r1 = requests.post(self.api_token, params=self.post_params, data=self.payload)
                print(r1.text)
                self.seq_count+=1
            except KeyboardInterrupt:
                print("{}Exiting. Last sequence sent = {} {}".format(YELLOW, self.seq_count, RESET))
                break
        self.save_config()

if __name__ == '__main__':
    zcc = ZoomClosedCaptions()