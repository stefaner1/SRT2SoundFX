import os, io, csv, json
import asyncio
from openai import AzureOpenAI, OpenAI
from itertools import islice

def get_openai_client():
    # Initialize the client based on available API key
    if os.getenv("OPENAI_API_KEY")!='':
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    else:
        client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version="2023-12-01-preview",
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        )
    return client

def chunk_elements(elements, each_chunk_size=40):
    it = iter(elements)
    for first in it:
        chunk = [first] + list(islice(it, each_chunk_size - 1))
        yield chunk


def convert_to_csv(elements):
    output = io.StringIO()
    fieldnames = ['ID', 'Text']
    writer = csv.DictWriter(output, fieldnames=fieldnames)

    writer.writeheader()
    for element in elements:
        writer.writerow({'ID': element['id'], 'Text': element['text']})

    return output.getvalue()

# Function to process 40 elements in one prompt
async def process_elements_chunks(elements):
    client = get_openai_client()
    texts = convert_to_csv(elements) # "\n".join([f"ID: {element['id']}, Text: {element['text']}" for element in elements])

    sleep_time = [0.1, 0.5, 1, 2, 3, 6]  # 6 times
    for minutes in sleep_time:  
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini" if isinstance(client, OpenAI) else "gpt-4o",
                messages=[
                    {"role": "system", "content": "You are an audiobook sound effect specialist."},
                    {
                        "role": "user",
                        "content": f"Below are {len(elements)} text snippets in CSV format. For each snippet, determine if a sound effect is really needed. If a sound effect is needed, specify what it should be and ensure it is a single, simple sound effect that includes the words 'high-quality'. \n" 
                        "REMEMBER: \n"
                        "1. Exclude sounds like speech (yelling, shouting, etc.), emotions, minor actions like 'looking', and any sounds that could last more than 22 seconds. \n"
                        "2. Prioritize quality over quantity—fewer, more impactful sounds are better. \n"
                        "3. Avoid repetition (e.g., if snippets 2 and 3 are similar, do not suggest sound effects for both). \n"
                        f"4. Ensure you return at least {int(len(elements) * 0.1)} sound effects. \n"
                        "-------\n\n TEXT SNIPPETS:\n"
                        f"{texts}\n\n -------"
                    }
                ],
                functions=[{
                    "name": "generate_prompt",
                    "description": "Generates prompts for sounds effects based on the provided text.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "elements": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "id": {"type": "integer", "description": "The ID of the element."},
                                        "prompt": {"type": "string", "description": "The sound effect description."},
                                        "duration": {"type": "number", "description": "The duration of the sound effect in seconds.", "minimum": 1, "maximum": 22}
                                    },
                                    "required": ["id", "prompt", "duration"]
                                }
                            }
                        },
                        "required": ["elements"]
                    }
                }]
                )

            # Extract the sound effects from the response
            if response.choices[0].message.content is not None and response.choices[0].message.function_call is None:
                # rerun the prompt
                prompts= await process_elements_chunks(elements)

            elif response.choices[0].message.function_call is not None:
                prompts = json.loads(response.choices[0].message.function_call.arguments)["elements"]
            else:
                prompts = []
            for prompt in prompts:
                prompt['text'] = next(element['text'] for element in elements if element['id'] == prompt['id'])
            return prompts

        except Exception as e:
            print(e)
            if 'Too Many Requests' in str(e) or 'RateLimitError' in str(e):
                time.sleep(minutes*60)
                continue
            try:
                if 'The response was filtered due to the prompt triggering Azure OpenAI\'s content management policy.' in str(e) or (response and "choices" in response and response.choices[0].finish_reason in ["content_filter", "stop"]):
                    return []
            except Exception as er:
                print(er)
            continue  # Continue to the next iteration of the loop in case of an exception
        raise Exception(f"Unsuccessful process_elements_chunks after few attempts. ARRAY TEXT: {str(chunk)}")


# Function to run all chunks in parallel with up to 8 processes
async def send_to_chatgpt(elements):
    chunks = list(chunk_elements(elements, 40))
    
    # Limit concurrency to 8 tasks
    semaphore = asyncio.Semaphore(8)
    
    async def sem_task(chunk):
        async with semaphore:
            return await process_elements_chunks(chunk)
    
    # Gather all the results
    results = await asyncio.gather(*[sem_task(chunk) for chunk in chunks])
    
    # Merge and sort results by 'id'
    merged_results = sorted([item for sublist in results for item in sublist], key=lambda x: x['id'])
    
    return merged_results
