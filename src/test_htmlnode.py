import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType, BlockType, text_node_to_html_node, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes, split_nodes_delimiter, block_to_block_type, markdown_to_html_node


class TestHTMLNode(unittest.TestCase):
    def test_props(self):
        node = HTMLNode(props={})
        node.props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        test_result = node.props_to_html()
        expected_result = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(test_result, expected_result)
    def test_props2(self):
        node = HTMLNode(props={})
        node.props = my_dict = {
        "name": "Luna",
        "age": 27,
        "city": "Helsinki",
        "is_student": False,
        "favorite_color": "blue"
        }

        test_result = node.props_to_html()
        expected_result = ' name="Luna" age="27" city="Helsinki" is_student="False" favorite_color="blue"'
        self.assertEqual(test_result, expected_result)
    def test_props3(self):
        node = HTMLNode(props={})
        node.props = my_dict = {
        "name": "Luna",
        "age": 27,
        "city": "Vaasa",
        "is_student": False,
        "favorite_color": "blue"
        }

        test_result = node.props_to_html()
        expected_result = ' name="Luna" age="27" city="Helsinki" is_student="False" favorite_color="blue"'
        self.assertNotEqual(test_result, expected_result)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Hello, world!")
        self.assertNotEqual(node.to_html(), "<p>Hello, world!</p>")   

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
    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("span", [child_node])
        self.assertNotEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )               
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    def test_bold(self):
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")
    
    def test_italic(self):
        node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")
        
    def test_code(self):
        node = TextNode("Code snippet", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "Code snippet")
        
    def test_link(self):
        node = TextNode("Link text", TextType.LINK, url="https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Link text")
        self.assertEqual(html_node.props, {"href": "https://example.com"})
        
    def test_image(self):
        node = TextNode("Alt text", TextType.IMAGE, url="image.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "image.jpg", "alt": "Alt text"}) 


    def test_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
                    TextNode("This is text with a ", TextType.TEXT),
                    TextNode("code block", TextType.CODE),
                    TextNode(" word", TextType.TEXT),
                ])
        
class TestSplitNodesDelimiter(unittest.TestCase):

    def test_bold_delimiter(self):
        input_node = TextNode("This is **bold** text", TextType.TEXT)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT)
        ]
        result = split_nodes_delimiter([input_node], "**", TextType.BOLD)
        self.assertEqual(result, expected)

    def test_code_delimiter(self):
        input_node = TextNode("Here is `inline code` example", TextType.TEXT)
        expected = [
            TextNode("Here is ", TextType.TEXT),
            TextNode("inline code", TextType.CODE),
            TextNode(" example", TextType.TEXT)
        ]
        result = split_nodes_delimiter([input_node], "`", TextType.CODE)
        self.assertEqual(result, expected)

    def test_italic_delimiter(self):
        input_node = TextNode("Some _italic_ text", TextType.TEXT)
        expected = [
            TextNode("Some ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT)
        ]
        result = split_nodes_delimiter([input_node], "_", TextType.ITALIC)
        self.assertEqual(result, expected)

    def test_no_delimiter(self):
        input_node = TextNode("Plain text with no formatting", TextType.TEXT)
        expected = [input_node]
        result = split_nodes_delimiter([input_node], "**", TextType.BOLD)
        self.assertEqual(result, expected)

    

    def test_multiple_nodes(self):
        input_nodes = [
            TextNode("This is **bold**", TextType.TEXT),
            TextNode(" and _italic_", TextType.TEXT)
        ]
        step1 = split_nodes_delimiter(input_nodes, "**", TextType.BOLD)
        result = split_nodes_delimiter(step1, "_", TextType.ITALIC)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC)
        ]
        self.assertEqual(result, expected)

    def test_empty_formatting(self):
        input_node = TextNode("Here is **** empty bold", TextType.TEXT)
        expected = [
            TextNode("Here is ", TextType.TEXT),
            TextNode("", TextType.BOLD),
            TextNode(" empty bold", TextType.TEXT)
        ]
        result = split_nodes_delimiter([input_node], "**", TextType.BOLD)
        self.assertEqual(result, expected)

class TestMarkdownExtraction(unittest.TestCase):

    def test_single_image(self):
        text = "Check this out ![cat](https://example.com/cat.png)"
        expected = [("cat", "https://example.com/cat.png")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_multiple_images(self):
        text = "![one](https://img1.png) and ![two](https://img2.png)"
        expected = [
            ("one", "https://img1.png"),
            ("two", "https://img2.png")
        ]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_image_and_link(self):
        text = "Here's an image ![img](https://img.png) and a [link](https://example.com)"
        image_expected = [("img", "https://img.png")]
        link_expected = [("link", "https://example.com")]
        self.assertEqual(extract_markdown_images(text), image_expected)
        self.assertEqual(extract_markdown_links(text), link_expected)

    def test_no_images(self):
        text = "Just a normal sentence."
        self.assertEqual(extract_markdown_images(text), [])

    def test_single_link(self):
        text = "Visit [Google](https://google.com)"
        expected = [("Google", "https://google.com")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_multiple_links(self):
        text = "[A](a.com) and [B](b.com)"
        expected = [("A", "a.com"), ("B", "b.com")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_image_link_does_not_match_link(self):
        text = "![Not a link](https://img.png)"
        self.assertEqual(extract_markdown_links(text), [])  # Should exclude images    

class TestSplitNodesImage(unittest.TestCase):

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    def test_multiple_links(self):
        node = TextNode("[Google](https://google.com) or [Bing](https://bing.com)", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [
            TextNode("Google", TextType.LINK, "https://google.com"),
            TextNode(" or ", TextType.TEXT),
            TextNode("Bing", TextType.LINK, "https://bing.com")
        ]
        self.assertEqual(result, expected)

    def test_link_and_image(self):
        node = TextNode("Link [site](url) and image ![alt](img)", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [
            TextNode("Link ", TextType.TEXT),
            TextNode("site", TextType.LINK, "url"),
            TextNode(" and image ![alt](img)", TextType.TEXT)  # image stays unprocessed here
        ]
        self.assertEqual(result, expected)
    def test_single_image(self):
        node = TextNode("Hello ![cat](https://img.com/cat.jpg) world", TextType.TEXT)
        result = split_nodes_image([node])
        expected = [
            TextNode("Hello ", TextType.TEXT),
            TextNode("cat", TextType.IMAGE, "https://img.com/cat.jpg"),
            TextNode(" world", TextType.TEXT)
    ]
        self.assertEqual(result, expected)

    def test_multiple_images(self):
        node = TextNode("Pics: ![one](url1) and ![two](url2)", TextType.TEXT)
        result = split_nodes_image([node])
        expected = [
            TextNode("Pics: ", TextType.TEXT),
            TextNode("one", TextType.IMAGE, "url1"),
            TextNode(" and ", TextType.TEXT),
            TextNode("two", TextType.IMAGE, "url2")
        ]
        self.assertEqual(result, expected)

    def test_image_only(self):
        node = TextNode("![logo](url)", TextType.TEXT)
        result = split_nodes_image([node])
        expected = [
            TextNode("logo", TextType.IMAGE, "url")
        ]
        self.assertEqual(result, expected)

    def test_heading_block(self):
        txt = "# This is a heading"
        self.assertEqual(block_to_block_type(txt), BlockType.HEADING)

    def test_code_block(self):
        txt = "```\nprint('Hello, World!')\n```"
        self.assertEqual(block_to_block_type(txt), BlockType.CODE)

    def test_quote_block(self):
        txt = "> This is a quote\n> Another quoted line"
        self.assertEqual(block_to_block_type(txt), BlockType.QUOTE)

    def test_unordered_list_block(self):
        txt = "- item 1\n- item 2\n- item 3"
        self.assertEqual(block_to_block_type(txt), BlockType.UNORDERED_LIST)

    def test_ordered_list_block(self):
        txt = "1. First item\n2. Second item\n3. Third item"
        self.assertEqual(block_to_block_type(txt), BlockType.ORDERED_LIST)

    def test_paragraph_block(self):
        txt = "This is just a normal paragraph without special markdown syntax."
        self.assertEqual(block_to_block_type(txt), BlockType.PARAGRAPH)

    def test_mixed_unordered_list_should_be_paragraph(self):
        txt = "- item 1\nnot a list item"
        self.assertEqual(block_to_block_type(txt), BlockType.PARAGRAPH)

    def test_mixed_ordered_list_should_be_paragraph(self):
        txt = "1. First item\nSomething random\n3. Third item"
        self.assertEqual(block_to_block_type(txt), BlockType.PARAGRAPH)

    def test_empty_input_returns_paragraph(self):
        txt = ""
        self.assertEqual(block_to_block_type(txt), BlockType.PARAGRAPH)

class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_paragraph(self):
        markdown = "This is a paragraph."
        html = markdown_to_html_node(markdown)
        self.assertEqual(html.tag, "div")
        self.assertEqual(html.children[0].tag, "p")

    def test_heading(self):
        markdown = "### Heading Level 3"
        html = markdown_to_html_node(markdown)
        self.assertEqual(html.children[0].tag, "h3")

    def test_blockquote(self):
        markdown = "> This is a quote."
        html = markdown_to_html_node(markdown)
        self.assertEqual(html.children[0].tag, "blockquote")

    def test_unordered_list(self):
        markdown = "- Item 1\n- Item 2\n- Item 3"
        html = markdown_to_html_node(markdown)
        self.assertEqual(html.children[0].tag, "ul")
        self.assertEqual(len(html.children[0].children), 3)
        self.assertTrue(all(child.tag == "li" for child in html.children[0].children))

    def test_ordered_list(self):
        markdown = "1. First\n2. Second\n3. Third"
        html = markdown_to_html_node(markdown)
        self.assertEqual(html.children[0].tag, "ol")
        self.assertEqual(len(html.children[0].children), 3)
        self.assertTrue(all(child.tag == "li" for child in html.children[0].children))

    def test_code_block(self):
        markdown = "```\nprint('Hello')\nprint('World')\n```"
        html = markdown_to_html_node(markdown)
        self.assertEqual(html.children[0].tag, "pre")
        self.assertEqual(html.children[0].children[0].tag, "code")
        self.assertEqual(html.children[0].children[0].children[0].text, "print('Hello')\nprint('World')")


    

if __name__ == "__main__":
    unittest.main()