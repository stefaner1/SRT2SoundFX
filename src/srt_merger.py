class SrtMerger:
    def __init__(self, chatgpt_prompts, srt_elements):
        self.srt_elements = srt_elements
        self.chatgpt_prompts = chatgpt_prompts

    def merge_prompts(self):
        merged_elements = []
        for prompt in self.chatgpt_prompts:
            srt_element = next(element for element in self.srt_elements if element['id'] == prompt['id'])
            merged_element = {
                    'start': srt_element['start'],
                    'end': srt_element['end'],
                    'prompt': prompt['prompt'],
                    'text': srt_element['text'],
                    'id': srt_element['id']
                }
            merged_elements.append(merged_element)

        return merged_elements