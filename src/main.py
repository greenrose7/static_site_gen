import re
from file_handling import copy_contents, generate_page

def main():
    #This first deletes the public directory    
    copy_contents("./static", "./public")
    generate_page("content/index.md", "template.html", "public/index.html")

main()