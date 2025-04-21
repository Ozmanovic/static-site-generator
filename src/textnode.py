from enum import Enum

class TextType(Enum):
    BOLD = "bold"
    ITALIC = "italic"
    STRIKETHROUGH = "strikethrough"
    INLINE_CODE = "code"
    LINK = "link"
    IMAGE = "image"
    BLOCK_QUOTE = "quote"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    def __eq__(self, value):
        self.value = value
        if self.text_type == value.text_type and self.text == value.text and self.url == value.url:
            return True 
    def __repr__(self):
        return(f"TextNode({self.text}, {self.text_type}, {self.url})")  
    