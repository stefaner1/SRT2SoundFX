class SrtMerger:
    def __init__(self, srt_elements, chatgpt_prompts):
        self.srt_elements = srt_elements
        self.chatgpt_prompts = chatgpt_prompts

    def merge_prompts(self):
        merged_elements = []
        for srt_element in self.srt_elements:
            for prompt in self.chatgpt_prompts:
                if srt_element['id'] == prompt['id']:
                    merged_element = {
                        'start': srt_element['start'],
                        'end': srt_element['end'],
                        'prompt': prompt['prompt']
                    }
                    merged_elements.append(merged_element)
        return merged_elements