import unittest

from textnode import TextNode, TextType
from main import text_node_to_html_node
from leafnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node1, node2)
    
    def test_full_eq(self):
        node1 = TextNode("This is a text node", TextType.CODE, "http://google.com")
        node2 = TextNode("This is a text node", TextType.CODE, "http://google.com")
        self.assertEqual(node1, node2)

    def test_textonly_eq(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node1, node2)
    
    def test_url_not_eq(self):
        node1 = TextNode("This is a text node", TextType.ITALIC, "http://google.com")
        node2 = TextNode("This is a text node", TextType.ITALIC, "http://yahoo.com")
        self.assertNotEqual(node1, node2)
    
    def test_one_url_set_not_eq(self):
        node1 = TextNode("This is a text node", TextType.ITALIC, "http://google.com")
        node2 = TextNode("This is a text node", TextType.ITALIC,)
        self.assertNotEqual(node1, node2)

    def test_text_node_to_html_bold(self):
        node1 = TextNode("This is a bold node", TextType.BOLD)
        node1 = text_node_to_html_node(node1)
        expected_outcome = LeafNode("b", "This is a bold node")
        self.assertEqual(node1, expected_outcome)
    
    def test_text_node_to_html_link(self):
        node1 = TextNode("This is a link node", TextType.LINK, "https://google.com")
        node1 = text_node_to_html_node(node1)
        expected_outcome = LeafNode("a", "This is a link node", {"href": "https://google.com"})
        self.assertEqual(node1, expected_outcome)
    
    def test_text_node_to_html_text(self):
        node1 = TextNode("This is a text node", TextType.TEXT)
        node1 = text_node_to_html_node(node1)
        expected_outcome = LeafNode(None, "This is a text node")
        self.assertEqual(node1, expected_outcome)
    
    def test_text_node_to_html_image(self):
        node1 = TextNode("This is a image node", TextType.IMAGE, "some/image/location")
        node1 = text_node_to_html_node(node1)
        expected_outcome = LeafNode("img", "", {"src": "some/image/location", "alt": "This is a image node"})
        self.assertEqual(node1, expected_outcome)
    
    def test_text_node_to_html_incorrect_textype(self):
        node1 = TextNode("This is a bogus node", "texttype")
        self.assertRaises(Exception, text_node_to_html_node, node1)

if __name__ == "__main__":
    unittest.main()