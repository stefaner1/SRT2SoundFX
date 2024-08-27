import os, json
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv

load_dotenv()

# https://elevenlabs.io/docs/api-reference/how-to-use-text-to-sound-effects

def generate_sounds(elements, project_name='audiobook'):
    """
    This function takes the new list of SRT elements from `merge_prompts` and generates sounds for each element using the ElevenLabs API.
    """
    elevenlabs = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

    sounds = []
    elements_to_process=[element for element in elements if not element.get("audio_path")]
    for idx, element in enumerate(elements_to_process):
        print("Generating sound effects...")
        try:
            result = elevenlabs.text_to_sound_effects.convert(
                text=element['prompt'],
                # duration_seconds=10,  # Optional, if not provided will automatically determine the correct length
                prompt_influence=0.3,  # Optional, if not provided will use the default value of 0.3
            )
            results_path=os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))),'resources')
            output_path = os.path.join(results_path, f"{project_name}_{element['id']}.mp3")
            with open(output_path, "wb") as f:
                for chunk in result:
                    f.write(chunk)
            elements[idx]["audio_path"]=output_path

            save_path = os.path.join(results_path, f"{project_name}_sounds.json")
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(elements, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Error generating sound for element {element['id']}: {e}")
            elements[idx]["audio_path"]=None
    return elements

def rerun_generate_sounds(project_name='audiobook'):
    # open the json file
    results_path=os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))),'resources')
    save_path = os.path.join(results_path, f"{project_name}_sounds.json")
    with open(save_path, 'r', encoding='utf-8') as f:
        elements = json.load(f)

    elements= generate_sounds(elements, project_name)
    return elements