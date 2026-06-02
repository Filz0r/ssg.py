class HTMLNode:
    def __init__(
            self,
            tag: str | None = None,
            value: str | None = None,
            children: list[HTMLNode] | None = None,
            props: dict[str,str] | None = None,
            ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"

    def to_html(self):
        raise NotImplementedError("This isn't implemented in the base class")
    
    def props_to_html(self):
        res = ""
        for k,v in self.props.items():
            template = '%key%="%value%"'
            res += template.replace("%key%", k).replace("%value%", v) + " "
        return res.rstrip()
