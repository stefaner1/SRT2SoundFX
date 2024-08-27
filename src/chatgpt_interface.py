import openai
# use gpt-4o mini
def send_to_chatgpt(elements):
    openai.api_key = 'your-api-key'

    prompts = []
    for element in elements:
        response = openai.Completion.create(
            engine="gpt-4o",
            prompt=f"I am an audiobook sound effect generator. Here is a text: {element['text']}",
        )
        prompts.append({
            'id': element['id'],
            'prompt': response.choices[0].text.strip()
        })

    return prompts