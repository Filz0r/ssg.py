from enum import Enum
from .leafnode import LeafNode

class TextType(Enum):
    PLAIN = "plain"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMG = "image"


class TextNode:
    def __init__(self, text:str, text_type: TextType, url: str | None = None):
        if not isinstance(text_type, TextType):
            raise ValueError(f"You can only pass an TextType argument as the text_type parameter, you passed {type(text_type)}")
        if (text_type == TextType.LINK or text_type == TextType.IMG) and url is None:
            raise ValueError("You cannot create an LINK or IMG node without passing an URL")
        if not (text_type == TextType.LINK or text_type == TextType.IMG) and url is not None:
            raise ValueError(f"You cannot pass url to a node of type {text_type.value}")
        self.text = text
        self.text_type: TextType = text_type
        self.url = url

    def __eq__(self, value):
        return self.text == value.text and self.text_type == value.text_type and self.url == value.url
    
    def __repr__(self):
        return f"TextNode(text={self.text}, text_type={self.text_type.value}, url={self.url})"
    

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match(text_node.text_type):
        case TextType.PLAIN:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMG:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})