import unittest

from main import markdown_to_blocks, block_to_block_type

class TestBlocks(unittest.TestCase):
### markdown_to_blocks
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

### block_to_block_type
    def test_block_to_block_type_heading_1(self):
        text = "# This is a level 1 heading!"
        self.assertEqual("heading1", block_to_block_type(text))
    
    def test_block_to_block_type_heading_3(self):
        text = "### This is a level 3 heading!"
        self.assertEqual("heading3", block_to_block_type(text))
    
    def test_block_to_block_type_heading_6(self):
        text = "###### This is a level 6 heading!"
        self.assertEqual("heading6", block_to_block_type(text))
    
    def test_block_to_block_type_heading_too_many(self):
        text = "######### This is a level 9 heading, which should be interpreted as a paragraph!"
        self.assertEqual("paragraph", block_to_block_type(text))
    
    def test_block_to_block_type_heading_no_space(self):
        text = "###This is a level 3 heading but lacks a space, which should be interpreted as a paragraph!"
        self.assertEqual("paragraph", block_to_block_type(text))
    
    def test_block_to_block_type_heading_code(self):
        text = '''```This is a block of code
It may have multiple lines of code
But ends with triple backtick```'''
        self.assertEqual("code", block_to_block_type(text))

    def test_block_to_block_type_heading_code_one_line(self):
        text = '''```This is a block of code all on one line```'''
        self.assertEqual("code", block_to_block_type(text))

    def test_block_to_block_type_heading_code_no_end(self):
        text = '''```This is a block of code
It may have multiple lines of code
This one lacks ending ticks, so will be a paragraph'''
        self.assertEqual("paragraph", block_to_block_type(text))
    
    def test_block_to_block_type_heading_code_2_ticks(self):
        text = '''``This is a block of code
It may have multiple lines of code
This one only has 2 ticks on each end, so will be a paragraph``'''
        self.assertEqual("paragraph", block_to_block_type(text))

    def test_block_to_block_type_quote(self):
        text = '''> This is a quote
> Each line must start with an >
> Or else!'''
        self.assertEqual("quote", block_to_block_type(text))
    
    def test_block_to_block_type_quote_one_line(self):
        text = '''> This is a quote of just one line'''
        self.assertEqual("quote", block_to_block_type(text))
    
    def test_block_to_block_type_quote_missing_gt_sign(self):
        text = '''> This is a quote
> Each line must start with an >
But this one doesn't, so this should be a paragraph!'''
        self.assertEqual("paragraph", block_to_block_type(text))
    
    def test_block_to_block_type_unordered_list(self):
        text = '''* This is an unordered list
* Each line must start with * or -
* It can be long
- As far as I know the symbols can be mixed
* So we will allow this :) '''
        self.assertEqual("unorderedlist", block_to_block_type(text))
        
    def test_block_to_block_type_unordered_list_no_spaces(self):
        text = '''- This is an unordered list
- Each line must start with * or -
-However there needs to be a space after each marker
- Since the line above doesn't have one, this will be a paragraph'''
        self.assertEqual("paragraph", block_to_block_type(text))
    
    def test_block_to_block_type_ordered_list(self):
        text = '''1. This is an ordered list
2. Each line must start with a sequential number, a ., then a space 
3. Another line
4. Line #4 '''
        self.assertEqual("orderedlist", block_to_block_type(text))

    def test_block_to_block_type_ordered_list_wrong_num(self):
        text = '''1. This is an ordered list
2. Each line must start with a sequential number, a ., then a space 
4. This line num is not sequential
5. So this is a paragraph '''
        self.assertEqual("paragraph", block_to_block_type(text))

    def test_block_to_block_type_ordered_list_wrong_start(self):
        text = '''2. This is an ordered list
3. Each line must start with a sequential number, a ., then a space 
4. This doesn't start at #1
5. So this is a paragraph '''
        self.assertEqual("paragraph", block_to_block_type(text))

    def test_block_to_block_type_ordered_list_missing_num(self):
        text = '''1. This is an ordered list
2. Each line must start with a sequential number, a ., then a space 
This doesn't have a number
3. So this is a paragraph '''
        self.assertEqual("paragraph", block_to_block_type(text))

    def test_block_to_block_type_ordered_list_missing_num_jumped(self):
        text = '''1. This is an ordered list
2. Each line must start with a sequential number, a ., then a space 
This doesn't have a number
4. So this is a paragraph '''
        self.assertEqual("paragraph", block_to_block_type(text))

    def test_block_to_block_type_ordered_list_missing_space(self):
        text = '''1. This is an ordered list
2. Each line must start with a sequential number, a ., then a space 
3.This line is missing its space at the start
4. So this is a paragraph '''
        self.assertEqual("paragraph", block_to_block_type(text))

    def test_block_to_block_type_paragraph(self):
        text = '''This is just a normal paragraph.
It may have multiple lines of text
There may be some stray characters > like these # ones
1. It shouldn't stop it from being a paragraph
* Still a paragraph'''
        self.assertEqual("paragraph", block_to_block_type(text))

if __name__ == "__main__":
    unittest.main()