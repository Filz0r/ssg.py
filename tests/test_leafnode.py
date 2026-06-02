import unittest
from src.leafnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_value_required(self):
        with self.assertRaises(ValueError):
            LeafNode()
    
    def test_repr(self):
        node = LeafNode("p", "Hello world")
        self.assertEqual(node.__repr__(), 'LeafNode(tag=p, value=Hello world, props=None)')