import unittest
from src.textnode import TextType, TextNode, text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("Hello world", TextType.PLAIN)
        node2 = TextNode("Hello world", TextType.PLAIN)

        self.assertEqual(node, node2)

    def test_not_equal(self):
        node = TextNode("Hello world", TextType.PLAIN)
        node2 = TextNode("Hello world!", TextType.PLAIN)

        self.assertNotEqual(node, node2)

    def test_not_equal2(self):
        node = TextNode("Hello world", TextType.PLAIN)
        node2 = TextNode("Hello world", TextType.BOLD)

        self.assertNotEqual(node, node2)

    def test_text_type_is_not_enum(self):
        with self.assertRaises(ValueError):
            TextNode("Hello fail!", "me fails")

    def test_text_type_is_enum(self):
        node = TextNode("Hello fail!", TextType.BOLD)
        self.assertEqual(node.text_type, TextType.BOLD)

    def test_ensure_url_is_required_when_required(self):
        with self.assertRaises(ValueError):
            TextNode("Hello fail!", TextType.LINK)

    def test_ensure_url_is_none_when_not_required(self):
        with self.assertRaises(ValueError):
            TextNode("Hello fail!", TextType.BOLD, "bla")

    def test_text(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")


    def test_italic_html(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.to_html(), "<i>This is a text node</i>")

    def test_link_html(self):
        node = TextNode("google", TextType.LINK, "https://google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), '<a href="https://google.com">google</a>')

    def test_link_html(self):
        node = TextNode("image", TextType.IMG, "https://google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), '<img src="https://google.com" alt="image"></img>')