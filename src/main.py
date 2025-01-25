from textnode import TextNode, TextType
from leafnode import LeafNode

def main():
    #textnode = TextNode("This is dummy text", TextType.ITALIC, "http://google.com")
    #print(textnode)
    pass

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("TextNode has no matching TextType")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        elif delimiter not in node.text:
            new_nodes.append(node)
        elif node.text.count(delimiter) < 2: #error catching for if string does not have closing delimiter
            raise Exception("String missing closing delimiter\n" + f"String: {node.text}\n" + f"Delimiter: {delimiter}")
        else:
            split_text = node.text.split(delimiter, 2)
            split_nodes = [
                TextNode(split_text[0], TextType.TEXT), 
                TextNode(split_text[1], text_type), 
                TextNode(split_text[2], TextType.TEXT)
                ]
            while TextNode("", TextType.TEXT) in split_nodes: #Inelegant way to clear empty strings caused by delimiters at the start or end
                split_nodes.remove(TextNode("", TextType.TEXT))
            
            new_nodes.extend(split_nodes_delimiter(split_nodes, delimiter, text_type))
    return new_nodes


main()