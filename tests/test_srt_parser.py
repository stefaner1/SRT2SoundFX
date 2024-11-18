import unittest
from src.srt2soundfx.srt_parser import parse_srt
import os

class TestSrtParser(unittest.TestCase):

    def test_parse_srt(self):
        # Test case: The function should return an array of elements. Each element should have an ID and text.
        current_path=os.path.dirname(os.path.realpath(__file__))
        srt_file = 'audiobook.srt'
        srt_path=os.path.join(current_path,"resources", srt_file)
        result = parse_srt(srt_path)
        
        # Assert that the result is a list
        self.assertIsInstance(result, list)
        
        # Assert that each element in the list is a dictionary with an 'id' and 'text' key
        for element in result:
            self.assertIsInstance(element, dict)
            self.assertIn('id', element)
            self.assertIn('text', element)

if __name__ == '__main__':
    unittest.main()