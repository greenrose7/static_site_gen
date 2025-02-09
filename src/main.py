import re
from file_handling import copy_contents, generate_page, generate_pages_recursive

def main():
    #This first deletes the public directory    
    copy_contents("./static", "./public")
    generate_pages_recursive("content", "template.html", "public")

main()