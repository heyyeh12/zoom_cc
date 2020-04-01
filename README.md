# Zoom Closed Captions

This is a simple Python script that uses speech recognition libraries to post [3rd-party closed captions for Zoom meetings](https://support.zoom.us/hc/en-us/articles/115002212983-Integrating-a-third-party-closed-captioning-service).

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)

## Installation

Assumes Python 3 and [PipEnv](https://pipenv-fork.readthedocs.io/en/latest/) are installed
```sh
git clone https://github.com/heyyeh12/zoom_cc.git
cd zoom_cc
pipenv install
```

## Usage

1. Enable closed captioning in Zoom settings. Refer to [Zoom Help Center for instructions](https://support.zoom.us/hc/en-us/articles/207279736-Getting-started-with-closed-captioning).

2. Start a meeting and get the API token
![Copy Zoom API token](ZoomClosedCaptions.png)

3. Configure settings.json for your Zoom meeting
- `zoom_api_token` = Paste the copied API token. If left empty, you'll be prompted for the token at runtime
- `seq_count` = 0 for a new meeting, unless you are restarting the script after already captioning for some time
- `lang` = language option in post request (only tested with 'en-US' so far)
- `mic_timeout` = listening timeout for recognizer

4. Start recognition script
```sh
# Using SpeechRecognizer Google Speech Recognition
pipenv run python speech_recognizer_closed_caption.py
# Using Google Cloud Speech API (NOTE: requires [GOOGLE_APPLICATION_CREDENTIALS](https://cloud.google.com/speech-to-text/docs/quickstart-client-libraries))
pipenv run python transcribe_streaming_infinite.py
```

5. When prompted, type `y` to load settings from `settings.config`. Otherwise paste API token and set sequence count via command line when prompted.

6. Use ctrl+C to exit. The `settings.json` will be updated with the last used token and sequence count in case the script needs to be restarted during a Zoom meeting.