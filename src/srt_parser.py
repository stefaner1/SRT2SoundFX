import re
from typing import List, Dict

def parse_srt(file_path: str) -> List[Dict[str, str]]:
    """
    Parse an SRT file into a list of dictionaries.
    Each dictionary contains 'id', 'start_time', 'end_time', and 'text' of a subtitle.
    """
    with open(file_path, 'r') as file:
        content = file.read()

    # Split content by two newlines to get each subtitle
    subtitles = re.split('\n\n', content)

    parsed_subtitles = []
    for subtitle in subtitles:
        lines = subtitle.split('\n')
        if len(lines) >= 3:
            id = lines[0]
            start_time, end_time = lines[1].split(' --> ')
            text = ' '.join(lines[2:])
            parsed_subtitles.append({
                'id': id,
                'start_time': start_time,
                'end_time': end_time,
                'text': text
            })

    return parsed_subtitles