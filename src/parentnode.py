from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag == None:
            raise ValueError("ParentNode must have tag")
        if self.children == None or len(self.children) == 0:
            raise ValueError("ParentNode must have children")
        
        html_string = ""
        #Add open tag (incl. props)
        html_string += f"<{self.tag}"
        html_string += self.props_to_html()
        html_string += ">"
        
        #Iterate through children and add between tags (recursively)
        for child in self.children:
            html_string += child.to_html()
        #Add close tag
        html_string += f"</{self.tag}>"

        return html_string
