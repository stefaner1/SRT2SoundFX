import os
import asyncio
from srt2soundfx.core import Srt2SoundFX
from dotenv import load_dotenv

def main():
    load_dotenv()
    # Initialize the Srt2SoundFX class
    srt2soundfx = Srt2SoundFX(
        elevenlabs_api_key=os.getenv("ELEVENLABS_API_KEY"),
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )

    # Define paths
    current_path = os.path.dirname(os.path.realpath(__file__))
    srt_path = os.path.join(current_path, "tests", "resources", "audiobook.srt")
    save_dir = os.path.join(current_path, "resources")
    project_name = "audiobook"
    audiobook_path = os.path.join(current_path, "tests", "resources", "audiobook.mp3")

    # If you only want the sounds without placing them in the audio
    sounds =  srt2soundfx.generate_sounds(srt_path, save_dir, project_name)
    print(sounds)

if __name__ == "__main__":
    main()