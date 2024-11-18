class SrtMerger:
    def __init__(self, chatgpt_prompts, srt_elements):
        self.srt_elements = srt_elements
        self.chatgpt_prompts = chatgpt_prompts

    def merge_prompts(self):
        merged_elements = []
        for prompt in self.chatgpt_prompts:
            srt_element = next(element for element in self.srt_elements if element['id'] == prompt['id'])
            merged_element = srt_element.copy()
            merged_element.update(prompt)

            merged_elements.append(merged_element)
        return merged_elements

    def format_timecode(self, seconds):
            milliseconds = int((seconds - int(seconds)) * 1000)
            total_seconds = int(seconds)
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            secs = total_seconds % 60
            timecode = f"{hours:02}:{minutes:02}:{secs:02},{milliseconds:03}"
            return timecode
            
    def create_srt_file(self, elements):
        result_srt = ''
        for idx, element in enumerate(elements):
            # Convert start and end times to timecodes
            element['start_timecode'] = self.format_timecode(element['start'])
            element['end_timecode'] = self.format_timecode(element['end'])
            # SRT indices start from 1
            result = f"{idx + 1}\n{element['start_timecode']} --> {element['end_timecode']}\n{element['prompt']}\n\n"
            result_srt += result
        # Uncomment below to write to a file
        # with open('greifen_r5.srt', 'w') as f:
        #     f.write(result_srt)

        return result_srt