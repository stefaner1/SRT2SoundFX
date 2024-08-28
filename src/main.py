from dotenv import load_dotenv
from srt_parser import parse_srt
from chatgpt_interface import send_to_chatgpt
from srt_merger import SrtMerger
from sound_generator import generate_sounds, rerun_generate_sounds
from audio_placer import AudioPlacer
import os, asyncio


# Load environment variables from .env file
load_dotenv()

def main():
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    srt_path=os.path.join(parent_dir, "resources", "audiobook.srt")
    audiobook_path=os.path.join(parent_dir, "resources", "audiobook.mp3")
    temp_dir=os.path.join(parent_dir, "resources")
    project_name='audiobook_v2'

    # if file project_name sounds.json exists
    results_path=os.path.join(parent_dir,'resources')
    save_path = os.path.join(results_path, f"{project_name}_sounds.json")
    if os.path.exists(save_path):
        sounds= rerun_generate_sounds(project_name)
    else:
        # Parse the SRT file
        srt_elements = parse_srt(srt_path)
        

        # Send each element to ChatGPT
        prompts = asyncio.run(send_to_chatgpt(srt_elements))

        # Filter and merge sound effect prompts with start and end times
        srt_merger = SrtMerger(prompts, srt_elements)
        merged_elements = srt_merger.merge_prompts()

        # Generate sounds for each element
        sounds = generate_sounds(merged_elements, project_name)

    # Place the generated audio on an MP3 timeline
    audio_placer=AudioPlacer()
    result = audio_placer.add_sounds_to_audio(audiobook_path, sounds, temp_dir, final_audiobook_name=f"{project_name}_final_with_effects.mp3", final_effects_name=f"{project_name}_effects.mp3")
if __name__ == "__main__":
    main()