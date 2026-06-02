from .htmlnode import HTMLNode

TEMPLATE = '<%tag%%props%>%value%</%tag%>'

class LeafNode(HTMLNode):
    def __init__(self, tag = None, value = None, props = None):
        if value is None:
            raise ValueError("Cannot create leaf node without a value")

        super().__init__(tag, value, None, props)

    def __repr__(self):
        return f"LeafNode(tag={self.tag}, value={self.value}, props={self.props})"

    def to_html(self):
        if self.tag is None:
            return self.value
        
        props = " " + self.props_to_html() if self.props else ""

        return TEMPLATE.replace("%tag%", self.tag).replace("%value%", self.value).replace("%props%", props)
    
