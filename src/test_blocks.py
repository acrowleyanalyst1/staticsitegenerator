import unittest

from blocks import (
    BlockType,
    block_to_block_type,
    markdown_to_blocks,
    markdown_to_html_node,
)


class TestMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""

        self.assertEqual(
            markdown_to_blocks(md),
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_heading(self):
        self.assertEqual(
            block_to_block_type("## Heading"),
            BlockType.HEADING,
        )

    def test_code(self):
        self.assertEqual(
            block_to_block_type("```\nprint('hi')\n```"),
            BlockType.CODE,
        )

    def test_quote(self):
        self.assertEqual(
            block_to_block_type("> one\n> two"),
            BlockType.QUOTE,
        )

    def test_unordered_list(self):
        self.assertEqual(
            block_to_block_type("- one\n- two"),
            BlockType.UNORDERED_LIST,
        )

    def test_ordered_list(self):
        self.assertEqual(
            block_to_block_type("1. one\n2. two\n3. three"),
            BlockType.ORDERED_LIST,
        )

    def test_paragraph(self):
        self.assertEqual(
            block_to_block_type("Just a normal paragraph."),
            BlockType.PARAGRAPH,
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here
"""

        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """```
This is text that should remain
the **same** even with inline stuff
```"""

        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div><pre><code>This is text that should remain\nthe **same** even with inline stuff</code></pre></div>",
        )


if __name__ == "__main__":
    unittest.main()
