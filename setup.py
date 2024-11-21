from setuptools import setup, find_packages

# Read the requirements from requirements.txt
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="srt2soundfx",
    version="1.0.2",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=requirements,
    description="An audiobook sound effect generator that transforms SRT files into immersive audio experiences. It parses SRT files, uses ChatGPT to create sound effect prompts, generates sounds via the ElevenLabs API, and syncs the audio on an MP3 timeline.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/stefaner1/SRT2SoundFX",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7'
)