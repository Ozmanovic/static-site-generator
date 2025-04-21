class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    def to_html(self):
        raise Exception(NotImplementedError)
    def props_to_html(self):
        empty = []
        for prop in self.props:
            value = self.props[prop]
            format =  f' {prop}="{value}"'
            empty.append(format)
        final_format = "".join(empty)     
        return final_format
    def __repr__(self):
        print(f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})")

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, props=props)
    def to_html(self):  
        if self.value == None or self.value == "":
            raise ValueError("LeafNode must have a non-empty value.")
        if self.tag == None: 
            return self.value
        else:
            if self.props:
                attributes = self.props_to_html()  
            else:
                attributes = ""

            html_string = f"<{self.tag}{attributes}>{self.value}</{self.tag}>"
            return html_string
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, children, props=props)
    def to_html(self):
        if not self.tag:
            raise ValueError("ParentNode must have a non-empty tag.") 
        if not self.children:
            raise ValueError("ParentNode must have a non-empty children.") 
        else:
            