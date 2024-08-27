# SRT2SoundFX

This project is an audiobook sound effect generator based on SRT files. It parses SRT files, sends the elements to ChatGPT for sound effect prompts, merges the prompts with the SRT elements, generates sounds using the ElevenLabs API, and places the audio on an MP3 timeline.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Docker Compose installed.


### Installing

The first step is to clone the repository:

```
$ git clone https://github.com/stefaner1/srt_2_sound_effects.git
```

Then, navigate to the project folder:

```
$ cd srt_2_sound_effects
```

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

## Running the Application

Navigate back to the src directory:

```
$ cd /app
```

Then, run the application:

```
$ python main.py
```

## Built With

* [Python](https://www.python.org/) - The programming language used
* [ChatGPT](https://openai.com/research/chatgpt) - Used to generate sound effect prompts
* [ElevenLabs API](https://www.eleven-labs.com/) - Used to generate sounds


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
