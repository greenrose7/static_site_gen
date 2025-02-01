import unittest

from htmlnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_eq(self):
        node1 = LeafNode("h1", "this is a test heading", {"lang": "en", "test": "true"})
        node2 = LeafNode("h1", "this is a test heading", {"lang": "en", "test": "true"})
        self.assertEqual(node1, node2)
    
    def test_to_html_no_props(self):
        node1 = LeafNode("p", "This is a paragraph of text.")
        expected_output = "<p>This is a paragraph of text.</p>"
        self.assertEqual(node1.to_html(), expected_output)
    
    def test_to_html_with_props(self):
        node1 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        expected_output = "<a href=\"https://www.google.com\">Click me!</a>"
        self.assertEqual(node1.to_html(), expected_output)
    
    def test_to_html_no_tag_with_props(self):
        node1 = LeafNode(None, "Unclickable!", {"href": "https://www.google.com"})
        expected_output = "Unclickable!"
        self.assertEqual(node1.to_html(), expected_output)
    
    def test_to_html_no_value(self):
        node1 = LeafNode("h2", None, {"lang": "en", "test": "true"})
        self.assertRaises(ValueError, node1.to_html)



if __name__ == "__main__":
    unittest.main()