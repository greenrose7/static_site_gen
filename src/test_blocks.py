import unittest

from main import markdown_to_blocks

class TestBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        text = '''# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item'''
        expected_outcome = ["# This is a heading",
                            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                             '''* This is the first list item in a list block
* This is a list item
* This is another list item''']
        self.assertEqual(markdown_to_blocks(text), expected_outcome)
    
    def test_markdown_to_blocks_extra_newlines(self):
        text = '''

# This is a heading



This is a paragraph of text. It has some **bold** and *italic* words inside of it.


* This is the first list item in a list block
* This is a list item
* This is another list item


'''
        expected_outcome = ["# This is a heading",
                            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                             '''* This is the first list item in a list block
* This is a list item
* This is another list item''']
        self.assertEqual(markdown_to_blocks(text), expected_outcome)

    def test_markdown_to_blocks_extra_spaces(self):
        text = '''    # This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.    

* This is the first list item in a list block
* This is a list item
* This is another list item      '''
        expected_outcome = ["# This is a heading",
                            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                             '''* This is the first list item in a list block
* This is a list item
* This is another list item''']
        self.assertEqual(markdown_to_blocks(text), expected_outcome)

if __name__ == "__main__":
    unittest.main()