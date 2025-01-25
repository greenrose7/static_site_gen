from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value == None:
            raise ValueError("LeafNode must have value")
        html_string = ""
        #Add open tag if needed (incl. props)
        if self.tag != None:
            html_string += f"<{self.tag}"
            html_string += self.props_to_html()
            html_string += ">"
        #Add value/text
        html_string += self.value
        #Add close tag if needed
        if self.tag != None:
            html_string += f"</{self.tag}>"
        
        return html_string