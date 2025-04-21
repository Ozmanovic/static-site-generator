import unittest

from htmlnode import HTMLNode, LeafNode


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
             

    

    

if __name__ == "__main__":
    unittest.main()