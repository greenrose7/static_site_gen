import unittest

from textnode import TextNode, TextType
from main import text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links
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

### text_node_to_html_node
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

### split_nodes_delimiter
    def test_split_nodes_single_bold(self):
        node1 = TextNode("This text has **bold text** within", TextType.TEXT)
        expected_output = [
            TextNode("This text has ", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode(" within", TextType.TEXT)
        ]
        self.assertEqual(split_nodes_delimiter([node1], "**", TextType.BOLD), expected_output)
    
    def test_split_nodes_single_italic(self):
        node1 = TextNode("This text has *italic text* within", TextType.TEXT)
        expected_output = [
            TextNode("This text has ", TextType.TEXT),
            TextNode("italic text", TextType.ITALIC),
            TextNode(" within", TextType.TEXT)
        ]
        self.assertEqual(split_nodes_delimiter([node1], "*", TextType.ITALIC), expected_output)
    
    def test_split_nodes_single_code(self):
        node1 = TextNode("This text has `code text` within", TextType.TEXT)
        expected_output = [
            TextNode("This text has ", TextType.TEXT),
            TextNode("code text", TextType.CODE),
            TextNode(" within", TextType.TEXT)
        ]
        self.assertEqual(split_nodes_delimiter([node1], "`", TextType.CODE), expected_output)

    def test_split_nodes_multi_bold(self):
        node1 = TextNode("This text has **multiple** different **bold texts** within", TextType.TEXT)
        expected_output = [
            TextNode("This text has ", TextType.TEXT),
            TextNode("multiple", TextType.BOLD),
            TextNode(" different ", TextType.TEXT),
            TextNode("bold texts", TextType.BOLD),
            TextNode(" within", TextType.TEXT)
        ]
        self.assertEqual(split_nodes_delimiter([node1], "**", TextType.BOLD), expected_output)
    
    def test_split_nodes_missing_close_delim(self):
        node1 = TextNode("This text has **bold text with a missing close delim within", TextType.TEXT)
        self.assertRaises(Exception, split_nodes_delimiter, [node1], "**", TextType.BOLD)
    
    def test_split_nodes_no_delim(self):
        node1 = TextNode("This text has no delimiters!", TextType.TEXT)
        expected_output = [TextNode("This text has no delimiters!", TextType.TEXT)]
        self.assertEqual(split_nodes_delimiter([node1], "**", TextType.BOLD), expected_output)
    
    def test_split_nodes_sequential_bold_then_italic(self):
        node1 = TextNode("This text has **bold text** then some *italic text* then **even more bold text!**", TextType.TEXT)
        expected_output = [
            TextNode("This text has ", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode(" then some ", TextType.TEXT),
            TextNode("italic text", TextType.ITALIC),
            TextNode(" then ", TextType.TEXT),
            TextNode("even more bold text!", TextType.BOLD)
        ]
        output = split_nodes_delimiter([node1], "**", TextType.BOLD)
        output = split_nodes_delimiter(output, "*", TextType.ITALIC)

        self.assertEqual(output, expected_output)
    
    def test_split_nodes_full_bold(self):
        node1 = TextNode("**This text is all bold text**", TextType.TEXT)
        expected_output = [
            TextNode("This text is all bold text", TextType.BOLD)
        ]
        self.assertEqual(split_nodes_delimiter([node1], "**", TextType.BOLD), expected_output)

### extract_markdown_images (emi)
    def test_emi(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(extract_markdown_images(text), [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])
    
### extract_markdown_links (eml)
    def test_eml(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(extract_markdown_links(text), [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])


if __name__ == "__main__":
    unittest.main()