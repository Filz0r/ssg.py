from .htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(
            self,
            tag: str = None,
            children: list[HTMLNode] = None,
            props: dict = None
            ):
        super().__init__(tag, None, children, props)

    def __repr__(self):
        return f"ParentNode(tag={self.tag}, children={self.children}, props={self.props})"
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("Error tag is missing on the ParentNode Class")
        
        if self.children is None:
            raise ValueError("Error cannot be a parrent if children is none")
        
        res = f"<{self.tag}>"
        for child in self.children:
            res += child.to_html()

        res += f"</{self.tag}>"
        return res