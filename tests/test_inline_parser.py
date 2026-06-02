import unittest

from src.inline_parser import (
    tokenize,
    parse_delimited,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    TokenType,
    Token,
    extract_markdown_links,
    extract_markdown_images,
    markdown_to_blocks
    )
from src.textnode import TextNode, TextType


class TestTokenize(unittest.TestCase):
    def test_plain_text(self):
        tokens = tokenize("hello world", "`")
        self.assertEqual(tokens, [Token(TokenType.TEXT, "hello world")])

    def test_code_delimiter(self):
        tokens = tokenize("a `b` c", "`")
        self.assertEqual(
            tokens,
            [
                Token(TokenType.TEXT, "a "),
                Token(TokenType.DELIMITER, "`"),
                Token(TokenType.TEXT, "b"),
                Token(TokenType.DELIMITER, "`"),
                Token(TokenType.TEXT, " c"),
            ],
        )

    def test_bold_delimiter(self):
        tokens = tokenize("a **b** c", "**")
        self.assertEqual(
            tokens,
            [
                Token(TokenType.TEXT, "a "),
                Token(TokenType.DELIMITER, "**"),
                Token(TokenType.TEXT, "b"),
                Token(TokenType.DELIMITER, "**"),
                Token(TokenType.TEXT, " c"),
            ],
        )

    def test_italic_star(self):
        tokens = tokenize("a *b* c", "*")
        self.assertEqual(
            tokens,
            [
                Token(TokenType.TEXT, "a "),
                Token(TokenType.DELIMITER, "*"),
                Token(TokenType.TEXT, "b"),
                Token(TokenType.DELIMITER, "*"),
                Token(TokenType.TEXT, " c"),
            ],
        )

    def test_italic_underscore(self):
        tokens = tokenize("a _b_ c", "_")
        self.assertEqual(
            tokens,
            [
                Token(TokenType.TEXT, "a "),
                Token(TokenType.DELIMITER, "_"),
                Token(TokenType.TEXT, "b"),
                Token(TokenType.DELIMITER, "_"),
                Token(TokenType.TEXT, " c"),
            ],
        )

    def test_multiple_sections(self):
        tokens = tokenize("**a** and **b**", "**")
        self.assertEqual(
            tokens,
            [
                Token(TokenType.DELIMITER, "**"),
                Token(TokenType.TEXT, "a"),
                Token(TokenType.DELIMITER, "**"),
                Token(TokenType.TEXT, " and "),
                Token(TokenType.DELIMITER, "**"),
                Token(TokenType.TEXT, "b"),
                Token(TokenType.DELIMITER, "**"),
            ],
        )

    def test_empty_string(self):
        self.assertEqual(tokenize("", "`"), [])

    def test_adjacent_delimiters(self):
        tokens = tokenize("``", "`")
        self.assertEqual(
            tokens,
            [
                Token(TokenType.DELIMITER, "`"),
                Token(TokenType.DELIMITER, "`"),
            ],
        )


class TestParseDelimited(unittest.TestCase):
    def test_simple_code(self):
        tokens = tokenize("a `b` c", "`")
        nodes = parse_delimited(tokens, "`", TextType.CODE)
        self.assertEqual(
            nodes,
            [
                TextNode("a ", TextType.PLAIN),
                TextNode("b", TextType.CODE),
                TextNode(" c", TextType.PLAIN),
            ],
        )

    def test_simple_bold(self):
        tokens = tokenize("a **b** c", "**")
        nodes = parse_delimited(tokens, "**", TextType.BOLD)
        self.assertEqual(
            nodes,
            [
                TextNode("a ", TextType.PLAIN),
                TextNode("b", TextType.BOLD),
                TextNode(" c", TextType.PLAIN),
            ],
        )

    def test_multiple_bold_sections(self):
        tokens = tokenize("**a** and **b**", "**")
        nodes = parse_delimited(tokens, "**", TextType.BOLD)
        self.assertEqual(
            nodes,
            [
                TextNode("a", TextType.BOLD),
                TextNode(" and ", TextType.PLAIN),
                TextNode("b", TextType.BOLD),
            ],
        )

    def test_unmatched_delimiter_raises(self):
        tokens = tokenize("a `b", "`")
        with self.assertRaises(ValueError) as ctx:
            parse_delimited(tokens, "`", TextType.CODE)
        self.assertIn("unmatched delimiter", str(ctx.exception))

    def test_empty_between_delimiters(self):
        tokens = tokenize("a `` b", "`")
        nodes = parse_delimited(tokens, "`", TextType.CODE)
        self.assertEqual(
            nodes,
            [
                TextNode("a ", TextType.PLAIN),
                TextNode(" b", TextType.PLAIN),
            ],
        )


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code(self):
        node = TextNode("This is text with a `code block` word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.PLAIN),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.PLAIN),
            ],
        )

    def test_bold(self):
        node = TextNode("This is **bolded phrase** in the middle", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.PLAIN),
                TextNode("bolded phrase", TextType.BOLD),
                TextNode(" in the middle", TextType.PLAIN),
            ],
        )

    def test_italic_underscore(self):
        node = TextNode("hello _world_ foo", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("hello ", TextType.PLAIN),
                TextNode("world", TextType.ITALIC),
                TextNode(" foo", TextType.PLAIN),
            ],
        )

    def test_non_plain_passed_through(self):
        node = TextNode("bold", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("bold", TextType.BOLD)])

    def test_unmatched_raises(self):
        node = TextNode("hello `code", TextType.PLAIN)
        with self.assertRaises(ValueError) as ctx:
            split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertIn("unmatched delimiter", str(ctx.exception))

    def test_no_delimiter_returns_plain(self):
        node = TextNode("just plain text", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("just plain text", TextType.PLAIN)])

    def test_multiple_plain_nodes(self):
        nodes = [
            TextNode("a `code1` b", TextType.PLAIN),
            TextNode("c `code2` d", TextType.PLAIN),
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("a ", TextType.PLAIN),
                TextNode("code1", TextType.CODE),
                TextNode(" b", TextType.PLAIN),
                TextNode("c ", TextType.PLAIN),
                TextNode("code2", TextType.CODE),
                TextNode(" d", TextType.PLAIN),
            ],
        )
 

class TestMarkdownLinkExtraction(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an [text](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("text", "https://i.imgur.com/zjjcJKZ.png")], matches)


    def test_extract_markdown_multiple_links(self):
        matches = extract_markdown_links(
            "This is text with an [text](https://i.imgur.com/zjjcJKZ.png) [text2](https://link2.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("text", "https://i.imgur.com/zjjcJKZ.png"), ("text2", "https://link2.com/zjjcJKZ.png")], matches)


class TestSplitNodesImage(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMG, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode("second image", TextType.IMG, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_no_images(self):
        node = TextNode("This is plain text with no images.", TextType.PLAIN)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_non_plain_pass_through(self):
        node = TextNode("bold text", TextType.BOLD)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_multiple_plain_nodes(self):
        nodes = [
            TextNode("a ![img1](url1) b", TextType.PLAIN),
            TextNode("c ![img2](url2) d", TextType.PLAIN),
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("a ", TextType.PLAIN),
                TextNode("img1", TextType.IMG, "url1"),
                TextNode(" b", TextType.PLAIN),
                TextNode("c ", TextType.PLAIN),
                TextNode("img2", TextType.IMG, "url2"),
                TextNode(" d", TextType.PLAIN),
            ],
            new_nodes,
        )


class TestSplitNodesLink(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.PLAIN),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.PLAIN),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            new_nodes,
        )

    def test_split_no_links(self):
        node = TextNode("This is plain text with no links.", TextType.PLAIN)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_split_non_plain_pass_through(self):
        node = TextNode("italic text", TextType.ITALIC)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_multiple_plain_nodes(self):
        nodes = [
            TextNode("a [link1](url1) b", TextType.PLAIN),
            TextNode("c [link2](url2) d", TextType.PLAIN),
        ]
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual(
            [
                TextNode("a ", TextType.PLAIN),
                TextNode("link1", TextType.LINK, "url1"),
                TextNode(" b", TextType.PLAIN),
                TextNode("c ", TextType.PLAIN),
                TextNode("link2", TextType.LINK, "url2"),
                TextNode(" d", TextType.PLAIN),
            ],
            new_nodes,
        )


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_empty_string(self):
        self.assertEqual(markdown_to_blocks(""), [])

    def test_single_block(self):
        md = "Just one paragraph"
        self.assertEqual(markdown_to_blocks(md), ["Just one paragraph"])

    def test_multiple_blank_lines(self):
        md = "Paragraph one\n\n\n\nParagraph two"
        self.assertEqual(
            markdown_to_blocks(md),
            ["Paragraph one", "Paragraph two"],
        )

    def test_leading_and_trailing_whitespace(self):
        md = "   Leading and trailing spaces   \n\n  Another block  "
        self.assertEqual(
            markdown_to_blocks(md),
            ["Leading and trailing spaces", "Another block"],
        )

    def test_extra_blank_lines_at_edges(self):
        md = "\n\nFirst block\n\nSecond block\n\n"
        self.assertEqual(
            markdown_to_blocks(md),
            ["First block", "Second block"],
        )