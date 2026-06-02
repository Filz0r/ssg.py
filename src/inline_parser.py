from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, auto
from .textnode import TextNode, TextType

import re


class TokenType(Enum):
    TEXT = auto()
    DELIMITER = auto()


@dataclass(frozen=True)
class Token:
    type: TokenType
    value: str


def tokenize(text: str, delimiter: str) -> list[Token]:
    """
    Scan *text* left-to-right and emit a flat list of Tokens.
    Every occurrence of *delimiter* is a DELIMITER token;
    everything else is a TEXT token.
    """
    tokens: list[Token] = []
    i = 0
    n = len(text)
    dlen = len(delimiter)

    while i < n:
        end = i + dlen
        if end <= n and text[i:end] == delimiter:
            tokens.append(Token(TokenType.DELIMITER, delimiter))
            i = end
        else:
            start = i
            while i < n:
                end = i + dlen
                if end <= n and text[i:end] == delimiter:
                    break
                i += 1
            tokens.append(Token(TokenType.TEXT, text[start:i]))

    return tokens


def parse_delimited(tokens: list[Token], delimiter: str, text_type: TextType) -> list[TextNode]:
    """
    Walk a token stream and convert matched *delimiter* pairs into *text_type* nodes.
    Unmatched delimiters raise ``ValueError``.  All other tokens become PLAIN nodes.
    """
    nodes: list[TextNode] = []
    i = 0

    while i < len(tokens):
        tok = tokens[i]

        if tok.type is TokenType.TEXT:
            if tok.value:
                nodes.append(TextNode(tok.value, TextType.PLAIN))
            i += 1
            continue

        # tok.type is DELIMITER and tok.value == delimiter (guaranteed by tokenize)
        j = i + 1
        content_parts: list[str] = []
        found = False

        while j < len(tokens):
            t = tokens[j]
            if t.type is TokenType.DELIMITER:
                found = True
                break
            content_parts.append(t.value)
            j += 1

        if not found:
            raise ValueError(f"Invalid markdown: unmatched delimiter {delimiter!r}")

        inner = "".join(content_parts)
        if inner:
            nodes.append(TextNode(inner, text_type))
        i = j + 1

    return nodes


def split_nodes_delimiter(
    old_nodes: list[TextNode],
    delimiter: str,
    text_type: TextType,
) -> list[TextNode]:
    """
    Process a list of TextNodes.

    Non-PLAIN nodes pass through untouched.  PLAIN nodes are tokenised and
    parsed for the given *delimiter* / *text_type* pair.
    """
    result: list[TextNode] = []
    for node in old_nodes:
        if node.text_type is not TextType.PLAIN:
            result.append(node)
            continue

        tokens = tokenize(node.text, delimiter)
        result.extend(parse_delimited(tokens, delimiter, text_type))

    return result

def extract_markdown_images(text):
    regex = r"!\[(.+?)\]\((.+?)\)"
    matches = re.findall(regex, text)
    return matches

def extract_markdown_links(text):
    regex = r"\[(.+?)\]\((.+?)\)"
    matches = re.findall(regex, text)
    return matches


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    result: list[TextNode] = []
    for node in old_nodes:
        if node.text_type is not TextType.PLAIN:
            result.append(node)
            continue

        text = node.text
        images = extract_markdown_images(text)
        if not images:
            result.append(node)
            continue

        current_index = 0
        for alt, url in images:
            markdown = f"![{alt}]({url})"
            idx = text.find(markdown, current_index)
            if idx == -1:
                continue

            before = text[current_index:idx]
            if before:
                result.append(TextNode(before, TextType.PLAIN))
            result.append(TextNode(alt, TextType.IMG, url))
            current_index = idx + len(markdown)

        after = text[current_index:]
        if after:
            result.append(TextNode(after, TextType.PLAIN))

    return result


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    result: list[TextNode] = []
    for node in old_nodes:
        if node.text_type is not TextType.PLAIN:
            result.append(node)
            continue

        text = node.text
        links = extract_markdown_links(text)
        if not links:
            result.append(node)
            continue

        current_index = 0
        for link_text, url in links:
            markdown = f"[{link_text}]({url})"
            idx = text.find(markdown, current_index)
            if idx == -1:
                continue

            before = text[current_index:idx]
            if before:
                result.append(TextNode(before, TextType.PLAIN))
            result.append(TextNode(link_text, TextType.LINK, url))
            current_index = idx + len(markdown)

        after = text[current_index:]
        if after:
            result.append(TextNode(after, TextType.PLAIN))

    return result


def text_to_textnodes(text: str) -> list[TextNode]:
    """
    Convert a raw string of markdown-flavoured text into a flat list of TextNodes.
    """
    nodes = [TextNode(text, TextType.PLAIN)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    return nodes


def markdown_to_blocks(markdown: str) -> list[str]:
    res = []
    splitted = markdown.split("\n\n")

    for paragraph in splitted:
        if len(paragraph) == 0:
            continue
        res.append(paragraph.strip())
    
    return res

