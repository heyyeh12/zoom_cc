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

class ZoomClosedCaptions:
    """
    Provides closed captions with SpeechRecognition libary via Zoom 3rd party clsoed caption API
    """

    def __init__(self):
        """
        Initialization
        """
        self.r = None 
        self.mic = None
        self.settings_file = "settings.json"
        self.api_token = ""
        self.seq_count = 0
        self.post_params = {'seq': str(self.seq_count), 'lang': 'en-US'}
        self.payload = ""
        self.mic_timeout = 30
        self.phrase_time_limit = 30

        # Command line colors
        self.RED = '\u001b[31m'
        self.GREEN = '\u001b[32m'
        self.YELLOW = '\u001b[33m'
        self.PURPLE = '\u001b[35m'
        self.CYAN = '\u001b[36m'
        self.RESET = '\u001b[0m' 

        if strtobool(input("{}Load settings from config? {}".format(self.PURPLE, self.RESET))):
            self.load_config()
        else:
            self.input_config()
        
        self.save_config()

    def __enter__(self):
        pass

    def __exit__(self, exception_type, exception_value, traceback):
        self.save_config()
        print("{}Exiting. Last sequence sent = {} {}".format(self.YELLOW, self.seq_count, self.RESET))

    def input_config(self):
        """
        Configure Zoom API settings from command line
        """
        # Command line input
        API_ENDPOINT = str(input(
            "{}Enter the API token from Zoom > Closed Caption > Use a 3rd party CC service:\n>>{}".format(self.PURPLE,self.RESET)))
        while not API_ENDPOINT or "http" not in API_ENDPOINT:
            API_ENDPOINT = str(input('>>'))

        i = input("{}Enter start sequence numer:\n>>{}".format(self.PURPLE,self.RESET))
        if not i:
            print("Using 0 by default")
            i = 0
        else:
            try:
                i = int(i)
            except ValueError:
                print("Invalid number, using 0 by default")
                i = 0
        self.api_token = API_ENDPOINT
        self.seq_count = i
    
    def load_config(self):
        """
        Load Zoom API settings from JSON file
        """
        with open(self.settings_file) as config_file:
            data = json.load(config_file)
        
        # Required parameters
        self.api_token = data['zoom_api_token']
        self.seq_count = data['seq_count']
        if not self.api_token:
            print("Missing API token from settings")
            self.input_config()

        # Optinal parameters
        if 'lang' in data and data['lang']:
            self.post_params['lang'] = data['lang']
        if 'mic_timeout' in data:
            self.mic_timeout = int(data['mic_timeout'])
        if 'phrase_time_limit' in data:
            self.phrase_time_limit = int(data['phrase_time_limit'])
        
    def save_config(self):
        """
        Save settings on exit
        """
        print("Updating {}".format(self.settings_file))
        with open(self.settings_file) as config_file:
            data = json.load(config_file)
        data['zoom_api_token'] = self.api_token
        data['seq_count'] = self.seq_count
        with open(self.settings_file, 'w') as outfile:
            json.dump(data, outfile, indent=4)

    def post_transcript(self, transcript):
        """
        POST transcript to Zoom
        """
        self.post_params['seq'] = str(self.seq_count)
        r1 = requests.post(self.api_token,
            params=self.post_params, data=transcript.encode('utf-8'),
            headers={'Content-type': 'text/plain; charset=utf-8'})
        print(r1.text)
        self.seq_count+=1

    def create_recognizer(self):
        """
        Create recognizer objects
        """
        self.r = sr.Recognizer()
        self.mic = sr.Microphone()

    def run(self):
        """
        Run speech recognition / POST loop
        """
        self.create_recognizer()
        while True:
            try:
                with self.mic as source:
                    print('Calibrating for ambient noise...')
                    self.r.adjust_for_ambient_noise(source)
                    print('Energy threshold={}'.format(self.r.energy_threshold))
                    print('{}Say something (or press ctrl+C to exit) {}'.format(self.PURPLE,self.RESET))
                    try:
                        audio = self.r.listen(source,
                            timeout=self.mic_timeout, phrase_time_limit=self.phrase_time_limit)
                        print('Transcribing...')
                        self.payload = self.r.recognize_google(audio, language=self.post_params['lang'])
                        #self.payload = r.recognize_sphinx(audio)
                    except KeyboardInterrupt:
                        break
                    except sr.WaitTimeoutError:
                        print("Timeout error, continuing...")
                        continue
                    except sr.UnknownValueError:
                        print("Nothing said, continuing...")
                        continue
                    except:
                        print('{}Unexpected error: {}{}'.format(self.RED, sys.exc_info()[0], self.RESET))
                        raise
                
                print("{} >> seq {}: {} {}".format(self.GREEN, self.seq_count, self.payload, self.RESET))
                self.post_transcript(self.payload)
            except KeyboardInterrupt:
                break

if __name__ == '__main__':
    zcc = ZoomClosedCaptions()
    with zcc:
        zcc.run()