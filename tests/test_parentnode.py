import unittest
from src.leafnode import LeafNode
from src.parentnode import ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
    )
        
    def test_error_no_tag(self):
        with self.assertRaises(ValueError):
            grandchild_node = LeafNode("b", "grandchild")
            tag = ParentNode(tag= None, children=[grandchild_node])
            tag.to_html()

    def test_error_no_children(self):
        with self.assertRaises(ValueError):
            tag = ParentNode(tag="p")
            tag.to_html()
