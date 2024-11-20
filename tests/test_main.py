import unittest
from unittest.mock import patch, MagicMock
import os
from dotenv import load_dotenv
from src.srt2soundfx.core import Srt2SoundFX  


class TestSrt2SoundFX(unittest.TestCase):
   
    def setUp(self):
        load_dotenv()
        current_path=os.path.dirname(os.path.realpath(__file__))
        srt_file = 'audiobook.srt'
        self.save_dir=os.path.join(current_path,"resources")
        self.srt_path=os.path.join(current_path,"resources", srt_file)
        self.audiobook_file=os.path.join(current_path,"resources", "audiobook.mp3")

        elevenlabs_api_key=os.getenv("ELEVENLABS_API_KEY")
        openai_api_key=os.getenv("OPENAI_API_KEY")  
        self.srt2soundfx = Srt2SoundFX(elevenlabs_api_key=elevenlabs_api_key, openai_api_key=openai_api_key)  
        


    
    def test_generate_sounds_only(self):  
        result = self.srt2soundfx.generate_sounds(self.srt_path, self.save_dir)

        self.assertIsNotNone(result)
        
        

    def test_generate_sounds_and_add_to_audio(self):
        result = self.srt2soundfx.generate_sounds(self.srt_path, self.save_dir, audiobook_path=self.audiobook_file)
        
        self.assertIsNotNone(result)

if __name__ == '__main__':
    unittest.main()
