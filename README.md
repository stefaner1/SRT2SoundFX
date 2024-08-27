# My Python Project

This project is an audiobook sound effect generator based on SRT files. It parses SRT files, sends the elements to ChatGPT for sound effect prompts, merges the prompts with the SRT elements, generates sounds using the ElevenLabs API, and places the audio on an MP3 timeline.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You need Python 3.7 or later to run the project. You can have multiple Python versions (2.x and 3.x) installed on the same system without problems.

In Ubuntu, Mint and Debian you can install Python 3 like this:

```
$ sudo apt-get install python3 python3-pip
```

For other Linux flavors, macOS and Windows, packages are available at

https://www.python.org/getit/

### Installing

The first step is to clone the repository:

```
$ git clone https://github.com/yourusername/my-python-project.git
```

Then, navigate to the project folder:

```
$ cd my-python-project
```

Next, install the dependencies:

```
$ pip install -r requirements.txt
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
$ cd ../src
```

Then, run the application:

```
$ python main.py
```

## Built With

* [Python](https://www.python.org/) - The programming language used
* [ChatGPT](https://openai.com/research/chatgpt) - Used to generate sound effect prompts
* [ElevenLabs API](https://www.eleven-labs.com/) - Used to generate sounds

## Authors

* **Your Name** - *Initial work* - [YourUsername](https://github.com/yourusername)

See also the list of [contributors](https://github.com/yourusername/my-python-project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc