import unittest

from extract_markdown import (
    extract_markdown_images,
    extract_markdown_links,
)


class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = (
            "This is text with a ![rick roll]"
            "(https://i.imgur.com/aKaOqIh.gif)"
        )
        matches = extract_markdown_images(text)
        self.assertEqual(
            [("rick roll", "https://i.imgur.com/aKaOqIh.gif")],
            matches,
        )

    def test_extract_multiple_images(self):
        text = (
            "![first](https://example.com/1.png) "
            "![second](https://example.com/2.jpg)"
        )
        matches = extract_markdown_images(text)
        self.assertEqual(
            [
                ("first", "https://example.com/1.png"),
                ("second", "https://example.com/2.jpg"),
            ],
            matches,
        )

    def test_extract_markdown_links(self):
        text = (
            "This is text with a [link](https://www.boot.dev) "
            "and [youtube](https://www.youtube.com/@bootdotdev)"
        )
        matches = extract_markdown_links(text)
        self.assertEqual(
            [
                ("link", "https://www.boot.dev"),
                ("youtube", "https://www.youtube.com/@bootdotdev"),
            ],
            matches,
        )

    def test_extract_multiple_links(self):
        text = (
            "[Google](https://google.com) "
            "[GitHub](https://github.com)"
        )
        matches = extract_markdown_links(text)
        self.assertEqual(
            [
                ("Google", "https://google.com"),
                ("GitHub", "https://github.com"),
            ],
            matches,
        )

    def test_links_ignore_images(self):
        text = (
            "![image](https://image.png) "
            "[link](https://boot.dev)"
        )
        matches = extract_markdown_links(text)
        self.assertEqual(
            [("link", "https://boot.dev")],
            matches,
        )


if __name__ == "__main__":
    unittest.main()
