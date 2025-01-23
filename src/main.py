from textnode import TextNode, TextType

def main():
    textnode = TextNode("This is dummy text", TextType.ITALIC, "http://google.com")
    print(textnode)

main()