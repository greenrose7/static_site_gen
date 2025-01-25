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
        for i in self.props:
            html_attributes += f" {i}=\"{self.props[i]}\""
        return html_attributes
    
    def __repr__(self):
        print(f"""
HTMLNode:
    tag: {self.tag}
    value: {self.value}
    children: {self.children}
    props: {self.props}
"""
        )
    
    def __eq__(self, other):
        return (self.tag == other.tag and 
                self.value == other.value and 
                self.children == other.children and
                self.props == other.props
                )