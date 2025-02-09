import unittest
from htmlnode import LeafNode, ParentNode
from markdown_blocks import markdown_to_html_node

class Testmarkdownpageconverter(unittest.TestCase):
    def test_markdownpageconverter(self):
        markdown = '''## Headers

# This is a Heading h1

## This is a Heading h2

###### This is a Heading h6

## Emphasis

*This text will be italic*  

**This text will be bold**  

This will be **bold** then *italic*

## Lists

### Unordered

* Item 1
* Item 2
* Item 3
* Item 4

### Ordered

1. Item 1
2. Item 2
3. Item 3

## Images

![This is an alt text.](/image/sample.webp)

## Links

You may be using [Markdown Live Preview](https://markdownlivepreview.com/).

## Blockquotes

> Markdown is a lightweight markup language with plain-text-formatting syntax, created in 2004 by John Gruber with Aaron Swartz.
> 

## Blocks of code

```
let message = 'Hello world';
alert(message);
```

'''
        node_hierarchy = ParentNode("div", [
            ParentNode("h2", [
                LeafNode(None, "Headers")
            ]),
            ParentNode("h1", [
                LeafNode(None, "This is a Heading h1")
            ]),
            ParentNode("h2", [
                LeafNode(None, "This is a Heading h2")
            ]),
            ParentNode("h6", [
                LeafNode(None, "This is a Heading h6")
            ]),
            ParentNode("h2", [
                LeafNode(None, "Emphasis")
            ]),
            ParentNode("p", [
                LeafNode("i", "This text will be italic"),
                #LeafNode(None, "  ")
            ]),
            ParentNode("p", [
                LeafNode("b", "This text will be bold"),
                #LeafNode(None, "  ")
            ]),
            ParentNode("p", [
                LeafNode(None, "This will be "),
                LeafNode("b", "bold"),
                LeafNode(None, " then "),
                LeafNode("i", "italic")
            ]),
            ParentNode("h2", [
                LeafNode(None, "Lists")
            ]),
            ParentNode("h3", [
                LeafNode(None, "Unordered")
            ]),
            ParentNode("ul", [
                ParentNode("li", [LeafNode(None, "Item 1")]),
                ParentNode("li", [LeafNode(None, "Item 2")]),
                ParentNode("li", [LeafNode(None, "Item 3")]),
                ParentNode("li", [LeafNode(None, "Item 4")]),
            ]),
                ParentNode("h3", [
                LeafNode(None, "Ordered")
            ]),
            ParentNode("ol", [
                ParentNode("li", [LeafNode(None, "Item 1")]),
                ParentNode("li", [LeafNode(None, "Item 2")]),
                ParentNode("li", [LeafNode(None, "Item 3")]),
            ]),
            ParentNode("h2", [
                LeafNode(None, "Images")
            ]),
            ParentNode("p", [
                LeafNode("img", "", {"alt": "This is an alt text.", "src": "/image/sample.webp"})
            ]),
            ParentNode("h2", [
                LeafNode(None, "Links")
            ]),
            ParentNode("p", [
                LeafNode(None, "You may be using "),
                LeafNode("a", "Markdown Live Preview", {"href": "https://markdownlivepreview.com/"}),
                LeafNode(None, ".")
            ]),
            ParentNode("h2", [
                LeafNode(None, "Blockquotes")
            ]),
            ParentNode("blockquote", [
                LeafNode(None, "Markdown is a lightweight markup language with plain-text-formatting syntax, created in 2004 by John Gruber with Aaron Swartz."),
            ]),
            ParentNode("h2", [
                LeafNode(None, "Blocks of code")
            ]),
            ParentNode("pre", [
                LeafNode("code", '''let message = 'Hello world';
alert(message);'''),
            ]),
        ])

        html = '''<div><h2>Headers</h2>
<h1>This is a Heading h1</h1>
<h2>This is a Heading h2</h2>
<h6>This is a Heading h6</h6>
<h2>Emphasis</h2>
<p><i>This text will be italic</i>  </p>
<p><b>This text will be bold</b>  </p>
<p>This will be <b>bold</b> then <i>italic</i></p>
<h2>Lists</h2>
<h3>Unordered</h3>
<ul>
<li>Item 1</li>
<li>Item 2</li>
<li>Item 3</li>
<li>Item 4</li>
</ul>
<h3>Ordered</h3>
<ol>
<li>Item 1</li>
<li>Item 2</li>
<li>Item 3</li>
</ol>
<h2>Images</h2>
<p><img alt="This is an alt text." src="/image/sample.webp"></p>
<h2>Links</h2>
<p>You may be using <a href="https://markdownlivepreview.com/">Markdown Live Preview</a>.</p>
<h2>Blockquotes</h2>
<blockquote>Markdown is a lightweight markup language with plain-text-formatting syntax, created in 2004 by John Gruber with Aaron Swartz.</blockquote>
<h2>Blocks of code</h2>
<pre><code>let message = 'Hello world';
alert(message);
</code></pre>
</div>'''

        compiled_markdown = markdown_to_html_node(markdown)
        for idx, x in enumerate(node_hierarchy.children):
            self.assertEqual(node_hierarchy.children[idx], compiled_markdown.children[idx])
        self.assertEqual(node_hierarchy, markdown_to_html_node(markdown))

if __name__ == "__main__":
    unittest.main()