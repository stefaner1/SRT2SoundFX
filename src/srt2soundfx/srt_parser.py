import re
from typing import List, Dict

def time_converter(time_str):
    hours, minutes, seconds = time_str.split(':')
    seconds, milliseconds = seconds.split(',')
    total_seconds = int(hours) * 3600 + int(minutes) * 60 + int(seconds) + int(milliseconds) / 1000
    return total_seconds

def parse_srt(file_path: str) -> List[Dict[str, str]]:
    """
    Parse an SRT file into a list of dictionaries.
    Each dictionary contains 'id', 'start', 'end', and 'text' of a subtitle.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Split content by two newlines to get each subtitle
    subtitles = re.split('\n\n', content)

    parsed_subtitles = []
    for subtitle in subtitles:
        lines = subtitle.split('\n')
        if len(lines) >= 3:
            id = int(lines[0].replace("\ufeff",""))
            start_time, end_time = lines[1].split(' --> ')
            if len(lines) > 1:
                text = ' \n'.join(lines[2:])
            else:
                text = ' '.join(lines[2:])    
            parsed_subtitles.append({
                'id': id,
                'start': time_converter(start_time),
                'end': time_converter(end_time),
                'text': text
            })

    return parsed_subtitles