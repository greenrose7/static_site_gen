import re
from file_handling import copy_contents

def main():
    #textnode = TextNode("This is dummy text", TextType.ITALIC, "http://google.com")
    #print(textnode)
    
    copy_contents("./static", "./public")
    pass

main()