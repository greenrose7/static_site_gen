import unittest

from textnode import TextNode, TextType


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


if __name__ == "__main__":
    unittest.main()