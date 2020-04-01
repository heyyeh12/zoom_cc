# Zoom Closed Captions

This is a simple Python script that uses speech recognition libraries to post [3rd-party closed captions for Zoom meetings](https://support.zoom.us/hc/en-us/articles/115002212983-Integrating-a-third-party-closed-captioning-service).

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)

## Installation

### 1. Install [Python3](https://www.python.org/downloads/)

### 2. Clone this git repo
```sh
git clone https://github.com/heyyeh12/zoom_cc.git
```
### 3. Install [PyAudio](http://people.csail.mit.edu/hubert/pyaudio/#downloads) system-dependent prerequisites

#### For Mac
Get [Hombrew](https://brew.sh/), then
```sh
brew install portaudio
```
#### For Ubuntu
```sh
sudo apt-get install python-pyaudio python3-pyaudio
```
#### For Windows
```
python -m pip install pyaudio
```

### 4. Get [PipEnv](https://pipenv-fork.readthedocs.io/en/latest/)
```sh
pip3 install pipenv
```

### 5. Use PipEnv to install other dependencies
```sh
cd zoom_cc
pipenv install
```


## Usage

1. Enable closed captioning in Zoom settings. Refer to [Zoom Help Center for instructions](https://support.zoom.us/hc/en-us/articles/207279736-Getting-started-with-closed-captioning).

2. Start a meeting and get the API token
![Copy Zoom API token](ZoomClosedCaptions.png) <!-- .element height="50%" width="50%" -->

3. Configure settings.json for your Zoom meeting
- `zoom_api_token` = Paste the copied API token. If left empty, you'll be prompted for the token at runtime
- `seq_count` = 0 for a new meeting, unless you are restarting the script after already captioning for some time
- `lang` = [language option](https://cloud.google.com/speech-to-text/docs/languages) in post request (e.g. 'en-US' for English, 'zh' for Chinese)
- `mic_timeout` = listening timeout for recognizer before resetting because nothing was said
- `phrase_time_limit` = speaking timeout before transcribing and posting to Zoom (set lower to update Zoom more often, higher for more continuous phrases)

4. Start recognition script

Using SpeechRecognizer Google Speech Recognition
```sh
pipenv run python speech_recognizer_closed_caption.py
```
(Experimental) Using Google Cloud Speech API. NOTE: requires setting up [GOOGLE_APPLICATION_CREDENTIALS](https://cloud.google.com/speech-to-text/docs/quickstart-client-libraries)
```sh
pipenv run python transcribe_streaming_infinite.py
```

5. When prompted, type `y` to load settings from `settings.config`. Otherwise paste API token and set sequence count via command line when prompted.

6. Check Zoom for transcriptions. Words should be appearing on the bottom of the screen and in the full transcript.
![Open Zoom Transcript](ZoomFullTranscript.png) <!-- .element height="50%" width="50%" -->

7. Use ctrl+C to exit. The `settings.json` will be updated with the last used token and sequence count in case the script needs to be restarted during a Zoom meeting.

## Other Useful Resources
- [SpeechRecognition Python module](https://github.com/Uberi/speech_recognition)
  - [microphone/recognizer settings](https://github.com/Uberi/speech_recognition/blob/master/reference/library-reference.rst)
- [Google Cloud Speech-to-Text API](https://cloud.google.com/speech-to-text/docs)