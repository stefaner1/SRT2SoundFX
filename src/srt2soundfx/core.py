from .srt_parser import parse_srt
from .chatgpt_interface import send_to_chatgpt
from .srt_merger import SrtMerger
from .sound_generator import generate_sounds, rerun_generate_sounds
from .audio_placer import AudioPlacer
import os, asyncio

class Srt2SoundFX:
    def __init__(self, elevenlabs_api_key=None, openai_api_key=None, azure_openai_api_key='', azure_openai_endpoint=''):
        # Error if not provided
        if not elevenlabs_api_key or not openai_api_key:
            raise ValueError("API keys must be provided.")

        # set dev variables
        os.environ['ELEVENLABS_API_KEY'] = elevenlabs_api_key
        os.environ['OPENAI_API_KEY'] = openai_api_key or ''
        os.environ['AZURE_OPENAI_API_KEY'] = azure_openai_api_key or ''
        os.environ['AZURE_OPENAI_ENDPOINT'] = azure_openai_endpoint or ''
        
    

    def generate_sounds(self, srt_path, save_dir, project_name="audiobook", audiobook_path=None):
        # Load environment variables from .env file

        # if file project_name sounds.json exists
        results_path = os.path.dirname(srt_path)
        save_path = os.path.join(results_path, f"{project_name}_sounds.json")
        if os.path.exists(save_path):
            sounds = rerun_generate_sounds(save_dir, project_name)
        else:
            # Parse the SRT file
            srt_elements = parse_srt(srt_path)

            # Send each element to ChatGPT
            prompts = asyncio.run(send_to_chatgpt(srt_elements))

            # Filter and merge sound effect prompts with start and end times
            srt_merger = SrtMerger(prompts, srt_elements)
            merged_elements = srt_merger.merge_prompts()

            # Generate sounds for each element
            sounds = generate_sounds(merged_elements, save_dir, project_name)

        if(audiobook_path == None):
            return sounds
        # Place the generated audio on an MP3 timeline
        audio_placer = AudioPlacer()
        result = audio_placer.add_sounds_to_audio(audiobook_path, sounds, save_dir, final_audiobook_name=f"{project_name}_final_with_effects.mp3", final_effects_name=f"{project_name}_effects.mp3")
        return result
