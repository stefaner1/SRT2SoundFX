import os, io, csv, json
import asyncio
from openai import AzureOpenAI
from itertools import islice

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2023-12-01-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
)

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
    texts = convert_to_csv(elements) # "\n".join([f"ID: {element['id']}, Text: {element['text']}" for element in elements])

    # API call to Azure OpenAI
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an audiobook sound effect specialist."},
            {
                "role": "user",
                "content": f"Below are {len(elements)} text snippets in CSV format. For each snippet, determine if a sound effect is really needed. If a sound effect is needed, specify what it should be. \n REMEMBER: \n1. Exclude sounds like speech (yelling, shouting etc.), emotions, minor actions like 'looking'. \n2. Prioritize quality over quantity—fewer, more impactful sounds are better. \n3. Avoid repetition (e.g., if snippets 2 and 3 are similar, do not suggest sounds effects for both). \n\n-------\n\n TEXT SNIPPETS:\n{texts}\n\n -------"
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
                                "prompt": {"type": "string", "description": "The sound effect description."}
                            },
                            "required": ["id", "prompt"]
                        }
                    }
                },
                "required": ["elements"]
            }
        }]
    )

    # Extract the sound effects from the response
    if response.choices[0].message.function_call is not None:
        prompts = json.loads(response.choices[0].message.function_call.arguments)["elements"]
    else:
        prompts = []
    for prompt in prompts:
        prompt['text'] = next(element['text'] for element in elements if element['id'] == prompt['id'])

    
    return prompts

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
