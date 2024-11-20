# SRT2SoundFX
[![PyPI package](https://img.shields.io/badge/pip%20install-srt2soundfx-brightgreen)](https://pypi.org/project/srt2soundfx/) [![version number](https://img.shields.io/pypi/v/srt2soundfx?color=green&label=version)](https://github.com/stefaner1/srt2soundfx/releases) ![License](https://img.shields.io/github/license/stefaner1/srt2soundfx?v=1.1)

This project is a sound effect generator for audiobooks, videos, and recordings based on SRT files. It parses SRT files, sends the elements to ChatGPT for sound effect prompts, merges the prompts with the SRT elements, generates sounds using the ElevenLabs API, and (optionally) places the audio on an MP3 timeline.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.



### Prerequisites

- Python 3.7+
- OpenAI API key (get it [here](https://platform.openai.com/settings/organization/api-keys))
- ElevenLabs API key (get it [here](https://elevenlabs.io/app/settings/api-keys/))
- `ffmpeg` (optional, for adding sounds to the audio file)

### Installing

Install the package using pip:

```bash
pip install srt2soundfx
```
### Using the Package in Your Code
Here is an example of how to use the Srt2SoundFX class in your code:

```python
from srt2soundfx.core import Srt2SoundFX

# Initialize the Srt2SoundFX class with your API keys
# Choose between Azure OpenAI and OpenAI by providing the respective API keys
srt2soundfx = Srt2SoundFX(
    elevenlabs_api_key='ELEVENLABS_API_KEY',
    openai_api_key='OPENAI_API_KEY', # Use this if you are using OpenAI
    azure_openai_api_key='AZURE_OPENAI_API_KEY', # Use this if you are using Azure OpenAI
    azure_openai_endpoint='AZURE_OPENAI_ENDPOINT' # Use this if you are using Azure OpenAI
)
# Define paths
srt_path = "/path/to/your/audio.srt"
save_dir = "/path/to/save/directory"
project_name = "your_project_name"
audio_path = "/path/to/your/audio.mp3"

# Process the audio
result = srt2soundfx.generate_sounds(srt_path, save_dir, project_name, audio_path)

# If you only want the sounds without placing them in the audio
sounds = srt2soundfx.generate_sounds(srt_path, save_dir, project_name)

```
### Supported Languages
The Srt2SoundFX project supports all languages that are supported by ChatGPT (e.g., English, Spanish, French, German, Polish, Italian, Portuguese, Chinese, Japanese, Korean, Russian, Hindi, and Arabic). This means you can process SRT files in any of these languages, and the sound effect prompts will be generated accordingly. Ensure that your SRT file is properly formatted and encoded in the language you intend to use.


## Example Usage
Here is a complete example:

```python
from srt2soundfx.core import Srt2SoundFX

# Initialize the Srt2SoundFX class
srt2soundfx = Srt2SoundFX(
    elevenlabs_api_key='ELEVENLABS_API_KEY',
    openai_api_key='OPENAI_API_KEY'
)

# Define paths
srt_path = "resources/audiobook.srt"
save_dir = "resources"
project_name = "audiobook"
audiobook_path = "resources/audiobook.mp3"

# Process the audio
result = srt2soundfx.generate_sounds(srt_path, save_dir, project_name, audiobook_path)

# If you only want the sounds without placing them in the audio
sounds = srt2soundfx.generate_sounds(srt_path, save_dir, project_name)

```
### Example Output 
#### Output of `sounds` Variable
When processing an SRT file, the result includes a list of sound effects with their details, such as the start and end times, the prompt used to generate the sound, and the path to the generated audio files:
```json
[
    {
        "id": 10,
        "start": 30.3,
        "end": 33.0,
        "text": "The silhouettes of ships loomed on the horizon.",
        "prompt": "A high-quality sound of distant ships at sea, creating an atmosphere of adventure.",
        "duration": 12,
        "audio_path": "/resources/audiobook_10.mp3"
    },
    {
        "id": 35,
        "start": 116.5,
        "end": 118.2,
        "text": "We'll board them immediately.",
        "prompt": "A high-quality sound of swords clashing, symbolizing a naval battle or abordage.",
        "duration": 5,
        "audio_path": "/resources/audiobook_35.mp3"
    }
]
```
#### Output of `result` Variable
If you process an audio file along with the SRT file, the result variable contains paths to the final audio files:

```json
{
    "effects": "/app/resources/final_audiobook_with_effects.mp3",
    "final_audio": "/app/resources/effects.mp3"
}
```
- `effects`: Path to the audiobook with the sound effects added.
- `final_audio`: Path to the standalone audio effects timeline.

## Example Results of End Product
Due to limitations of the ElevenLabs API, sound effects longer than 22 seconds were added manually, and some sound effects were deleted. Below are examples of audiobooks where this tool was used:

[Audiobook in German](https://www.youtube.com/watch?v=RZadKUaIZcs&t=283)

[Audiobook in Polish](https://www.youtube.com/watch?v=1sAAcvZulqA&t=236)

## To-Do List

* [ ] Add other options for sound effects generation like open source: [AudioLDM](https://github.com/haoheliu/AudioLDM)
* [ ] Add option to select open source Llama LLM or similar for creating sound effects prompts
* [ ] Set predefined sound effects library to speed things up for short video reels

## Developing

First, clone the repository:


```bash
git clone https://github.com/stefaner1/SRT2SoundFX.git
```

Then, navigate to the project folder:

```
$ cd SRT2SoundFX
```

Set Up Environment Variables

Copy the .env_example file and rename it to .env:

```bash
cp .env_example .env
```
Open the .env file and set your API keys. Save the file. These variables will be automatically loaded during development.



Next, run docker:

```
$ docker-compose up
```

## Running the Tests

Navigate to the tests directory:

```
$ cd tests
```

Then, run the tests:

```
$ python -m unittest discover
```


## Built With

* [Python](https://www.python.org/) - The programming language used
* [ChatGPT](https://openai.com/research/chatgpt) - Used to generate sound effect prompts
* [ElevenLabs API](https://www.eleven-labs.com/) - Used to generate sounds


## License

This project is licensed under the MIT License.
