import unittest

from src.blocks import BlockType, block_to_block_type


class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Heading 2"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)

    def test_heading_without_space(self):
        self.assertEqual(block_to_block_type("#NoSpace"), BlockType.PARAGRAPH)

    def test_heading_too_many_hashes(self):
        self.assertEqual(block_to_block_type("####### Too many"), BlockType.PARAGRAPH)

    def test_code_block(self):
        block = "```\nsome code\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_block_inline(self):
        self.assertEqual(block_to_block_type("```inline```"), BlockType.CODE)

    def test_code_block_not_closed(self):
        self.assertEqual(block_to_block_type("```\nnot closed"), BlockType.PARAGRAPH)

    def test_quote_block(self):
        block = ">> Quote line one\n> Quote line two"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_block_no_space(self):
        block = ">>Quote\n>No space"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_block_missing_prefix(self):
        block = ">> Quote line\nNot quoted"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_list(self):
        block = "- Item one\n- Item two\n- Item three"
        self.assertEqual(block_to_block_type(block), BlockType.U_LIST)

    def test_unordered_list_missing_space(self):
        block = "-Item one\n- Item two"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_list_missing_prefix(self):
        block = "- Item one\nNot an item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list(self):
        block = "1. First\n2. Second\n3. Third"
        self.assertEqual(block_to_block_type(block), BlockType.O_LIST)

    def test_ordered_list_single_item(self):
        self.assertEqual(block_to_block_type("1. Only"), BlockType.O_LIST)

    def test_ordered_list_out_of_order(self):
        block = "1. First\n3. Third"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_wrong_start(self):
        block = "2. Second\n3. Third"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_missing_dot_space(self):
        block = "1.First\n2. Second"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraph(self):
        self.assertEqual(block_to_block_type("Just a plain paragraph."), BlockType.PARAGRAPH)

    def test_paragraph_with_inline_markdown(self):
        self.assertEqual(block_to_block_type("This has **bold** and `code`."), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()
