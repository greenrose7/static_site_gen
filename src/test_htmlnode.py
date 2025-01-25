import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node1 = HTMLNode("p", "this is a test paragraph", None, {"lang": "en", "test": "true"})
        node2 = HTMLNode("p", "this is a test paragraph", None, {"lang": "en", "test": "true"})
        self.assertEqual(node1, node2)
    
    def test_props_to_html(self):
        node1 = HTMLNode("a", "this is a test link", None, {"href": "https://www.google.com", "target": "_blank"})
        expected_output = " href=\"https://www.google.com\" target=\"_blank\""
        self.assertEqual(node1.props_to_html(), expected_output)
    
    def test_defaults(self):
        node1 = HTMLNode(None, None, None, None)
        node2 = HTMLNode()
        self.assertEqual(node1, node2)


if __name__ == "__main__":
    unittest.main()