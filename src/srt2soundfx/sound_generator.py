import os, json
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv

load_dotenv()

# https://elevenlabs.io/docs/api-reference/how-to-use-text-to-sound-effects

import concurrent.futures

def generate_sound_effect(element, idx, save_dir, project_name='audiobook'):
    if element.get("audio_path"):
        return element["audio_path"], idx

    elevenlabs = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
    try:
        result = elevenlabs.text_to_sound_effects.convert(
            text=element['prompt'],
            duration_seconds=element["duration"],  # Optional, if not provided will automatically determine the correct length
            prompt_influence=0.3,  # Optional, if not provided will use the default value of 0.3
        )
        output_path = os.path.join(save_dir, f"{project_name}_{element['id']}.mp3")
        with open(output_path, "wb") as f:
            for chunk in result:
                f.write(chunk)
        return output_path, idx
    except Exception as e:
        print(f"Error generating sound for element {element['id']}: {e}")
        return None, idx

def generate_sounds(elements, save_dir, project_name='audiobook', max_workers=5):
    """
    This function takes the new list of SRT elements from `merge_prompts` and generates sounds for each element using the ElevenLabs API.
    """

    # Use ThreadPoolExecutor with a maximum of 5 workers for concurrent execution
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit tasks to the executor
        futures = {executor.submit(generate_sound_effect, element, idx, save_dir, project_name): idx for idx, element in enumerate(elements)}

        # Collect results as tasks complete
        for future in concurrent.futures.as_completed(futures):
            index = futures[future]
            output_path, idx = future.result()
            elements[idx]["audio_path"] = output_path  # Store the result in the correct order
            # Save
            results_path=os.path.join(save_dir,'resources')
            save_path = os.path.join(results_path, f"{project_name}_sounds.json")
            
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(elements, f, ensure_ascii=False, indent=4)

    return elements
def rerun_generate_sounds(save_dir, project_name='audiobook'):
    # open the json file
    save_path = os.path.join(save_dir, f"{project_name}_sounds.json")
    with open(save_path, 'r', encoding='utf-8') as f:
        elements = json.load(f)

    elements= generate_sounds(elements, project_name)
    return elements