from .htmlnode import HTMLNode
from .inline_parser import text_to_textnodes, markdown_to_blocks
from .blocks import block_to_block_type, BlockType
from .textnode import TextNode, TextType, text_node_to_html_node
from .parentnode import ParentNode
from .leafnode import LeafNode


def text_to_children(text: str) -> list[HTMLNode]:
    """Convert inline markdown text into a list of HTMLNode children."""
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]


def block_to_html_node(block: str) -> HTMLNode:
    """Convert a single markdown block into an HTMLNode."""
    block_type = block_to_block_type(block)

    match block_type:
        case BlockType.PARAGRAPH:
            text = block.replace("\n", " ")
            children = text_to_children(text)
            return ParentNode("p", children)

        case BlockType.HEADING:
            space_idx = block.find(" ")
            level = space_idx
            text = block[space_idx + 1:]
            children = text_to_children(text)
            return ParentNode(f"h{level}", children)

        case BlockType.CODE:
            # Strip opening and closing fences (```)
            stripped = block.strip()
            code_text = stripped[3:-3].strip("\n")
            code_node = text_node_to_html_node(TextNode(code_text, TextType.CODE))
            return ParentNode("pre", [code_node])

        case BlockType.QUOTE:
            lines = block.split("\n")
            stripped_lines = []
            for line in lines:
                if line.startswith("> "):
                    stripped_lines.append(line[2:])
                elif line.startswith(">"):
                    stripped_lines.append(line[1:])
                else:
                    stripped_lines.append(line)
            text = " ".join(stripped_lines)
            children = text_to_children(text)
            return ParentNode("blockquote", children)

        case BlockType.U_LIST:
            items = []
            for line in block.split("\n"):
                text = line[2:]
                children = text_to_children(text)
                items.append(ParentNode("li", children))
            return ParentNode("ul", items)

        case BlockType.O_LIST:
            items = []
            for line in block.split("\n"):
                text = line.split(". ", 1)[1]
                children = text_to_children(text)
                items.append(ParentNode("li", children))
            return ParentNode("ol", items)

        case _:
            raise ValueError(f"Unknown block type: {block_type}")


def markdown_to_html_node(markdown: str) -> HTMLNode:
    """Convert a full markdown document into a single parent <div> HTMLNode."""
    blocks = markdown_to_blocks(markdown)
    children = [block_to_html_node(block) for block in blocks]
    return ParentNode("div", children)
