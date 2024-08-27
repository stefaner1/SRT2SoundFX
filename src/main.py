from srt_parser import parse_srt
from chatgpt_interface import send_to_chatgpt
from srt_merger import merge_prompts
from sound_generator import generate_sounds
from audio_placer import place_audio

def main():
    # Parse the SRT file
    srt_elements = parse_srt('path_to_your_srt_file')

    # Send each element to ChatGPT
    prompts = send_to_chatgpt(srt_elements)

    # Filter and merge sound effect prompts with start and end times
    merged_elements = merge_prompts(srt_elements, prompts)

    # Generate sounds for each element
    sounds = generate_sounds(merged_elements)

    # Place the generated audio on an MP3 timeline
    place_audio(sounds, 'path_to_your_mp3_file')

if __name__ == "__main__":
    main()