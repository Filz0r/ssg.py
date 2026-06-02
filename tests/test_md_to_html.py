import unittest
from src.md_to_html import markdown_to_html_node, text_to_children, block_to_html_node


class TestMarkdownToHtml(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code`
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code></p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>",
        )

    def test_heading(self):
        md = "# Heading 1\n\n## Heading 2 with **bold**"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2 with <b>bold</b></h2></div>",
        )

    def test_quote(self):
        md = "> This is a quote\n> with **bold** text"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote with <b>bold</b> text</blockquote></div>",
        )

    def test_unordered_list(self):
        md = "- item 1\n- item 2 with _italic_\n- item 3"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>item 1</li><li>item 2 with <i>italic</i></li><li>item 3</li></ul></div>",
        )

    def test_ordered_list(self):
        md = "1. first\n2. second with `code`\n3. third"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>first</li><li>second with <code>code</code></li><li>third</li></ol></div>",
        )

    def test_mixed_document(self):
        md = """# Title

This is a paragraph with a [link](https://boot.dev).

```
code block
```

> A quote

- list item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Title</h1><p>This is a paragraph with a <a href=\"https://boot.dev\">link</a>.</p><pre><code>code block</code></pre><blockquote>A quote</blockquote><ul><li>list item</li></ul></div>",
        )

    def test_empty_markdown(self):
        md = ""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div></div>")

    def test_single_paragraph(self):
        md = "Just a paragraph"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><p>Just a paragraph</p></div>")

    def test_text_to_children(self):
        children = text_to_children("Hello **world**")
        self.assertEqual(len(children), 2)
        self.assertEqual(children[0].to_html(), "Hello ")
        self.assertEqual(children[1].to_html(), "<b>world</b>")

    def test_block_to_html_node_heading(self):
        node = block_to_html_node("## Heading")
        self.assertEqual(node.to_html(), "<h2>Heading</h2>")

    def test_block_to_html_node_code(self):
        node = block_to_html_node("```\nfoo = 1\n```")
        self.assertEqual(node.to_html(), "<pre><code>foo = 1</code></pre>")

    def test_block_to_html_node_quote_single_line(self):
        node = block_to_html_node("> A quote")
        self.assertEqual(node.to_html(), "<blockquote>A quote</blockquote>")


if __name__ == "__main__":
    unittest.main()
