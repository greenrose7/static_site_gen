class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        html_attributes = ""
        if self.props == None:
            return html_attributes
        for i in self.props:
            html_attributes += f" {i}=\"{self.props[i]}\""
        return html_attributes
    
    def __repr__(self):
        print(f"""
HTMLNode:
    tag: {self.tag} type: {type(self.tag)}
    value: "{self.value}"
    children: {self.children}
    props: {self.props}
"""
        )
    
    def __eq__(self, other):
        return (self.tag == other.tag and 
                self.value == other.value and 
                self.compare_children(other) and
                self.props == other.props
                )
    
    def compare_children(self, other):
        if self.children == None and other.children == None:
            return True
        if self.children == None and other.children != None:
            return False
        if self.children != None and other.children == None:
            return False
        if len(self.children) != len(other.children):
            return False
        same_children = True
        for idx, val in enumerate(self.children):
            if self.children[idx] != other.children[idx]:
                same_children = False
        return same_children

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