from main import markdown_to_blocks, block_to_block_type, text_to_textnodes, text_node_to_html_node
from parentnode import ParentNode
from leafnode import LeafNode
from textnode import TextNode

def markdown_to_html_node(markdown):
    ## Split in to blocks
    block_strings = markdown_to_blocks(markdown)

    ## Determine block type
    ## Create HTMLNode 
    ## Create and assign child HTMLNodes based on block type
    block_nodes = []
    for block_string in block_strings:
        block_type = block_to_block_type(block_string)
        match block_type:
            case "heading1" | "heading2" | "heading3" | "heading4" | "heading5" | "heading6":
                block_string = block_string.lstrip("# ")
                leaf_nodes = text_to_leaf_nodes(block_string)
                block_node = ParentNode(f"{block_type[0]}{block_type[-1]}", leaf_nodes)
            case "code":
                block_string = block_string[3:-3]
                block_string = block_string.strip("\n")
                #leaf_nodes = text_to_leaf_nodes(block_string)
                sub_node = LeafNode("code", block_string)
                block_node = ParentNode("pre", [sub_node])
            case "quote":
                sub_nodes = clean_quote_syntax(block_string)
                block_node = ParentNode("blockquote", sub_nodes)
            case "unorderedlist":
                block_node = ParentNode("ul", split_lists(block_string, False))
            case "orderedlist":
                block_node = ParentNode("ol", split_lists(block_string, True))
            case "paragraph":
                block_node = ParentNode("p", text_to_leaf_nodes(block_string))
            case _:
                raise Exception(f"Block has no matching block type: {block_to_block_type(block_string)}")
        block_nodes.append(block_node)
    ## Assign all blocks to parent <div> HTMLNode
    parent_div = ParentNode("div", block_nodes)
    return parent_div

def split_lists(list :str, ordered :bool = False, tag = "li"):
    nodes = []
    split_lines = list.split("\n")
    for line in split_lines:
        if ordered:
            line = line[3:]
        else:
            line = line[2:]
        leaf_nodes = text_to_leaf_nodes(line)
        nodes.append(ParentNode(tag, leaf_nodes))
    return nodes

def clean_quote_syntax(text :str):
    nodes = []
    for line in text.split("\n"):
        line = line[1:]
        line = line.lstrip(" ")
        if line != "":
            leaf_nodes = text_to_leaf_nodes(line)
            nodes.append(ParentNode("p", leaf_nodes))
    return nodes


def text_to_leaf_nodes(text):
    text_nodes = text_to_textnodes(text)
    leaf_nodes = []
    for text_node in text_nodes:
        leaf_nodes.append(text_node_to_html_node(text_node))
    return leaf_nodes