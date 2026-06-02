import unittest
from src.builder import Builder


class TestBuilder(unittest.TestCase):
    def test_extract_title_simple(self):
        md = "# Hello"
        self.assertEqual(Builder.extract_title(md), "Hello")

    def test_extract_title_with_whitespace(self):
        md = "#   Hello World  "
        self.assertEqual(Builder.extract_title(md), "Hello World")

    def test_extract_title_no_h1(self):
        md = "## Heading 2\nSome text"
        with self.assertRaises(Exception) as context:
            Builder.extract_title(md)
        self.assertEqual(str(context.exception), "No h1 header found")

    def test_extract_title_no_header_at_all(self):
        md = "Just a paragraph"
        with self.assertRaises(Exception) as context:
            Builder.extract_title(md)
        self.assertEqual(str(context.exception), "No h1 header found")

    def test_extract_title_mixed_blocks(self):
        md = "Some intro text\n\n# The Title\n\nMore content"
        self.assertEqual(Builder.extract_title(md), "The Title")


if __name__ == "__main__":
    unittest.main()
