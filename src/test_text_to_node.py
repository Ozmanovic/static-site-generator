import unittest
from textnode import TextNode, TextType, text_node_to_html_node, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes, split_nodes_delimiter, markdown_to_blocks

class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_node_bold(self):
        text = "This is **bold** text"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_text_to_node_italic(self):
        text = "This is _italic_ text"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_text_to_node_code(self):
        text = "This is `code` text"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_text_to_node_link(self):
        text = "This is a [link](https://example.com) text"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_text_to_node_image(self):
        text = "This is an ![image](https://example.com/img.png) text"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/img.png"),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_text_to_node_multiple_formats(self):
        text = "**Bold** and _italic_ and `code` and [link](https://example.com)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("Bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
        ]
        self.assertEqual(result, expected)

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
    def test_single_paragraph(self):
        md = "This is a simple paragraph with no breaks."
        expected = ["This is a simple paragraph with no breaks."]
        self.assertEqual(markdown_to_blocks(md), expected)

    def test_paragraphs_split_by_blank_line(self):
        md = """First paragraph.

        Second paragraph."""
        expected = ["First paragraph.", "Second paragraph."]
        self.assertEqual(markdown_to_blocks(md), expected)

    def test_trailing_and_leading_whitespace(self):
        md = """

        
        First paragraph with space.    

    
        Second paragraph.    
        
        
        """
        expected = [
            "First paragraph with space.",
            "Second paragraph.",
        ]
        self.assertEqual(markdown_to_blocks(md), expected)

    def test_heading_and_paragraph(self):
        md = """# Heading 1

        This is some text below a heading.
        """
        expected = [
            "# Heading 1",
            "This is some text below a heading.",
        ]
        self.assertEqual(markdown_to_blocks(md), expected)

    def test_list_block(self):
        md = """
        - Item 1
        - Item 2
        - Item 3
        """
        expected = ["- Item 1\n- Item 2\n- Item 3"]
        self.assertEqual(markdown_to_blocks(md), expected)

    def test_empty_input(self):
        md = ""
        expected = []
        self.assertEqual(markdown_to_blocks(md), expected)

    def test_only_newlines(self):
        md = "\n\n\n"
        expected = []
        self.assertEqual(markdown_to_blocks(md), expected)

    def test_mixed_block_types(self):
        md = """# Title

        Paragraph with _italic_ and **bold**

        - First
        - Second
        - Third
        """
        expected = [
            "# Title",
            "Paragraph with _italic_ and **bold**",
            "- First\n- Second\n- Third"
        ]
        self.assertEqual(markdown_to_blocks(md), expected)