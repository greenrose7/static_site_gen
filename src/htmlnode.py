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

