import re

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

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        elif len(extract_markdown_images(node.text)) == 0:
            #print("No links found")
            new_nodes.append(node)
        else:
            image_tuples = extract_markdown_images(node.text)
            alt_text, image_link = image_tuples[0]
            split_text = node.text.split(f"![{alt_text}]({image_link})", 1)
            split_nodes = [
                TextNode(split_text[0], TextType.TEXT), 
                TextNode(alt_text, TextType.IMAGE, image_link), 
                TextNode(split_text[1], TextType.TEXT)
                ]
            while TextNode("", TextType.TEXT) in split_nodes: #Inelegant way to clear empty strings caused by delimiters at the start or end
                split_nodes.remove(TextNode("", TextType.TEXT))
            if split_nodes[-1].text_type == TextType.TEXT:
                new_nodes.extend(split_nodes_image(split_nodes))
            else:
                new_nodes.extend(split_nodes)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        elif len(extract_markdown_links(node.text)) == 0:
            #print("No links found")
            new_nodes.append(node)
        else:
            link_tuples = extract_markdown_links(node.text)
            alt_text, url_link = link_tuples[0]
            split_text = node.text.split(f"[{alt_text}]({url_link})", 1)
            split_nodes = [
                TextNode(split_text[0], TextType.TEXT), 
                TextNode(alt_text, TextType.LINK, url_link), 
                TextNode(split_text[1], TextType.TEXT)
                ]
            while TextNode("", TextType.TEXT) in split_nodes: #Inelegant way to clear empty strings caused by delimiters at the start or end
                split_nodes.remove(TextNode("", TextType.TEXT))
            if split_nodes[-1].text_type == TextType.TEXT:
                new_nodes.extend(split_nodes_link(split_nodes))
            else:
                new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text):
    found_patterns = re.findall(r"!\[.+?\]\(.+?\)", text)
    if len(found_patterns) < 1:
        return []
    image_tuples = []
    for pattern in found_patterns:
        stripped = pattern.strip("![)]")
        split = stripped.split("](")
        image_tuples.append(tuple(split))
    return image_tuples

def extract_markdown_links(text):
    found_patterns = re.findall(r"\[.+?\]\(.+?\)", text)
    if len(found_patterns) < 1:
        return []
    link_tuples = []
    for pattern in found_patterns:
        stripped = pattern.strip("[)]")
        split = stripped.split("](")
        link_tuples.append(tuple(split))
    return link_tuples

def text_to_textnodes(text):
    text_nodes = [TextNode(text, TextType.TEXT)]
    text_nodes = split_nodes_image(text_nodes)
    text_nodes = split_nodes_link(text_nodes)
    text_nodes = split_nodes_delimiter(text_nodes, "**", TextType.BOLD)
    text_nodes = split_nodes_delimiter(text_nodes, "*", TextType.ITALIC)
    text_nodes = split_nodes_delimiter(text_nodes, "`", TextType.CODE)
    
    return text_nodes

main()