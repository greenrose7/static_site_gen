from inline_markdown import text_to_textnodes
from htmlnode import ParentNode, LeafNode
from textnode import text_node_to_html_node

def markdown_to_blocks(markdown):
    string_blocks = []
    current_block = ""
    for string in markdown.split("\n"):
        if string != "":
            if current_block != "":
                current_block += "\n"
            current_block += string
        else:
            if current_block != "":
                string_blocks.append(current_block.strip(" "))
                current_block = ""
    if current_block != "":
        string_blocks.append(current_block.strip(" "))
    return string_blocks

def block_to_block_type(markdown_text):
    match markdown_text[0]:
        case '#': #Headings
            count = 0
            while markdown_text[count] == '#' and count < 6: #counting num of #
                count += 1
            if markdown_text[count] == " ": #making sure next character is a space, else invalid
                return f"heading{count}" 
        
        case '`': #Code
            if markdown_text.startswith('```') and markdown_text.endswith('```'):
                return "code"
            
        case '>': #Quote
            split_text = markdown_text.split("\n")
            all_quotes = True
            for line in split_text:
                if line[0] != '>':
                    all_quotes = False
            if all_quotes: return "quote"

        case '*' | "-": #Unordered list
            split_text = markdown_text.split("\n")
            all_lists = True
            for line in split_text:
                if not line.startswith('* ') and not line.startswith('- '):
                    all_lists = False
            if all_lists: return "unorderedlist"

        case '1': #Ordered list
            split_text = markdown_text.split("\n")
            all_lists = True
            current_number = 1
            for line in split_text:
                if line.startswith(f"{current_number}. ") == False:
                    all_lists = False
                current_number += 1
            if all_lists: return "orderedlist"

        case _: #Normal Paragraph
            pass
    
    return "paragraph" #additional catch all if case above doesn't meet secondary conditions

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

def clean_quote_syntax(text :str, use_paragraphs = False):
    nodes = []
    for line in text.split("\n"):
        line = line[1:]
        line = line.lstrip(" ")
        if line != "":
            leaf_nodes = text_to_leaf_nodes(line)
            if use_paragraphs:
                nodes.append(ParentNode("p", leaf_nodes))
            else:
                nodes.extend(leaf_nodes)
    return nodes


def text_to_leaf_nodes(text):
    text_nodes = text_to_textnodes(text)
    leaf_nodes = []
    for text_node in text_nodes:
        leaf_nodes.append(text_node_to_html_node(text_node))
    return leaf_nodes

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block_string in blocks:
        if block_to_block_type(block_string) == "heading1":
            return block_string.strip("# ")
    raise Exception("No Header 1 Found")
        