import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_non_eq(self):
        node = TextNode("This is a text monkey", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2) 
    def test_url(self):       
        node = TextNode("This is a text node", TextType.BOLD, url=None)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    def test_url2(self):       
        node = TextNode("This is a text node", TextType.BOLD, url="google.com")
        node2 = TextNode("This is a text node", TextType.BOLD, url="google.com")
        self.assertEqual(node, node2)
    def test_url3(self):       
        node = TextNode("This is a text node", TextType.BOLD, url="gemini.com")
        node2 = TextNode("This is a text node", TextType.BOLD, url="google.com")
        self.assertNotEqual(node, node2)
    def test_text_type(self):
        node = TextNode("This is a text node", TextType.ITALIC, url="google.com")
        node2 = TextNode("This is a text node", TextType.BOLD, url="google.com")
        self.assertNotEqual(node, node2)

  
   



    

if __name__ == "__main__":
    unittest.main()