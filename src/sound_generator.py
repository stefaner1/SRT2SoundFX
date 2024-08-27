import requests

def generate_sounds(srt_elements):
    """
    This function takes the new list of SRT elements from `merge_prompts` and generates sounds for each element using the ElevenLabs API.
    """
    sounds = []
    for element in srt_elements:
        response = requests.post('https://api.elevenlabs.com/generate-sound', data = element['prompt'])
        if response.status_code == 200:
            sounds.append(response.json())
        else:
            print(f"Failed to generate sound for element {element['id']}")
    return sounds