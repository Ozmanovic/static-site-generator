from enum import Enum
from htmlnode import LeafNode, HTMLNode, ParentNode

import re

class TextType(Enum):
    BOLD = "bold"
    ITALIC = "italic"
    STRIKETHROUGH = "strikethrough"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"
    BLOCK_QUOTE = "quote"
    TEXT = "normal"
    

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    def __eq__(self, value):
        if self.text_type == value.text_type and self.text == value.text and self.url == value.url:
            return True 
        else:
            return False
        
    def __repr__(self):
        return(f"TextNode({self.text}, {self.text_type}, {self.url})") 
     
def text_node_to_html_node(text_node):   
    if not isinstance(text_node, TextNode):
        raise Exception("Input is not a TextNode")
    else:
        if text_node.text_type == TextType.TEXT:
            return LeafNode(tag=None, value=text_node.text)
        elif text_node.text_type == TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        elif text_node.text_type == TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        elif text_node.text_type == TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        elif text_node.text_type == TextType.STRIKETHROUGH:
            return LeafNode(tag="s", value=text_node.text)
        elif text_node.text_type == TextType.LINK:
            link_props = {
                "href": text_node.url,
            }
            return LeafNode(tag="a", value=text_node.text, props=link_props)
        elif text_node.text_type == TextType.IMAGE:
            image_props = {
                "src": text_node.url,
                "alt": text_node.text
            }
            return LeafNode(tag="img", value=" ", props=image_props)
        elif text_node.text_type == TextType.BLOCK_QUOTE:
            return LeafNode(tag="blockquote", value=text_node.text)
        else:
            raise Exception(f"Invalid text type: {text_node.text_type}")
        
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    
    new_list = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_list.append(node)
            continue

        text = node.text
        i = 0
        buffer = ""
        in_formatting = False
        delimiter_len = len(delimiter)

        while i < len(text):
            if text[i:i + delimiter_len] == delimiter:
                if in_formatting:
                    # Closing formatting block
                    print(f"Debug - text_type: {text_type}, buffer: {buffer}")  # Debug line
                    new_list.append(TextNode(buffer, text_type))
                    print(f"✅ Created formatted node: '{buffer}' as {text_type}")

                    buffer = ""
                    in_formatting = False
                else:
                    # Opening formatting block
                    if buffer:
                        new_list.append(TextNode(buffer, TextType.TEXT))
                    buffer = ""
                    in_formatting = True
                i += delimiter_len
            else:
                buffer += text[i]
                i += 1

        # Flush buffer
        if buffer:
            if in_formatting:
                # If we're still in formatting mode at the end, treat it as regular text with the delimiter
                new_list.append(TextNode(delimiter + buffer, TextType.TEXT))
            else:
                new_list.append(TextNode(buffer, TextType.TEXT))

    return new_list

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)  
            continue
        text = node.text
        matches = re.finditer(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
        last_index = 0
        
        
        
        for match in matches:
            no_img = text[last_index: match.start()]
            if no_img:

                new_nodes.append(TextNode(no_img, TextType.TEXT,))  
            

            alt = match.group(1)
            url = match.group(2)

                
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            last_index = match.end()
                
        

    
        if last_index < len(text):
            remaining = text[last_index:] 
            new_nodes.append(TextNode(remaining, TextType.TEXT,))
                    
        
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)  
            continue

        text = node.text
        matches = re.finditer(r"(?<!!)\[([^\[\]]+)\]\(([^()]+)\)", text)
        last_index = 0
        
        
        
        for match in matches:
            no_img = text[last_index: match.start()]
            if no_img:
                new_nodes.append(TextNode(no_img, TextType.TEXT,))  
            

            alt = match.group(1)
            url = match.group(2)

                
            new_nodes.append(TextNode(alt, TextType.LINK, url))
            last_index = match.end()
                
        

    
        if last_index < len(text):
            remaining = text[last_index:] 
            new_nodes.append(TextNode(remaining, TextType.TEXT,))
                    
    return new_nodes
    
def text_to_textnodes(text):
    # Start with a single text node
    nodes = [TextNode(text, TextType.TEXT)]
    
    # Process delimiters in sequence
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_image(nodes)
    
    return nodes


def markdown_to_blocks(markdown_text):
    list_str = []

    splitted = markdown_text.split("\n\n")
    for split in splitted:
        
            
        stripped_block = split.strip()
        if stripped_block != "":
        
        
            lines = stripped_block.split("\n")
            clean_lines = []
            for line in lines:
                clean_lines.append(line.strip())
            clean_block = "\n".join(clean_lines)
            
            list_str.append(clean_block)
    
    return list_str
    
class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(txt):
    lines = txt.split('\n')
    
  
    if txt.startswith("#"):
        return BlockType.HEADING
    
    
    if txt.startswith("```") and txt.endswith("```"):
        return BlockType.CODE
    
    
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    
   
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    
    ordered_list = True
    for i, line in enumerate(lines, 1):
        parts = line.split('. ', 1)
        if len(parts) != 2 or not parts[0].isdigit() or int(parts[0]) != i:
            ordered_list = False
            break
    if ordered_list and lines:  
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocked_md = markdown_to_blocks(markdown)
    html_list = []
    for block in blocked_md:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            children = text_to_textnode_to_htmlnode(block)
            html_list.append(ParentNode(tag="p", children=children, props={}))
        elif block_type == BlockType.QUOTE:
            # Remove the '>' characters from the beginning of each line
            cleaned_block = "\n".join(line.lstrip("> ") for line in block.split("\n"))
            children = text_to_textnode_to_htmlnode(cleaned_block)
            html_list.append(ParentNode(tag="blockquote", children=children, props={}))
        elif block_type == BlockType.UNORDERED_LIST:
            children = []
            splitted_list = block.split("\n")
            for line in splitted_list:
                if line.startswith("- "):
                    content = line[2:].strip()
                    processed = text_to_textnode_to_htmlnode(content)
                    children.append(ParentNode(tag="li", children=processed))
                else:
                    continue
        

            
            html_list.append(ParentNode(tag="ul", children=children, props={}))
        elif block_type == BlockType.ORDERED_LIST:
            children = []
            splitted_list = block.split("\n")
            for line in splitted_list:

                if re.match(r"^\d+\.\s", line):
                    content = re.sub(r"^\d+\.\s", "", line)
                    processed = text_to_textnode_to_htmlnode(content)
                    children.append(ParentNode(tag="li", children=processed))
                else:
                    continue
            
            html_list.append(ParentNode(tag="ol", children=children, props={}))
        elif block_type == BlockType.HEADING:
            # Count the hashtags
            match = re.match(r'^(#+)\s', block)
            if match:
                level = len(match.group(1))
                # Remove the hashtags and space
                content = re.sub(r'^#+\s', '', block)
                children = text_to_textnode_to_htmlnode(content)
                html_list.append(ParentNode(tag=f"h{level}", children=children, props={}))
        elif block_type == BlockType.CODE:
            # Strip leading/trailing whitespace and remove the triple backticks
            lines = block.split("\n")
            # Skip the first and last line (which contain ```)
            code_content = "\n".join(lines[1:-1])
            # Create a text node without processing markdown
            text_node = TextNode(code_content, TextType.TEXT, None)
            leaf_node = text_node_to_html_node(text_node)
            html_node = ParentNode(tag="code", children=[leaf_node], props={})
            pre_node = ParentNode(tag="pre", children=[html_node], props={})
            html_list.append(pre_node)
        
    return ParentNode(tag="div", children=html_list)    

def text_to_textnode_to_htmlnode(text):
    html_nodes = []
    txt_nodes = text_to_textnodes(text)
    for node in txt_nodes:

        html_nodes.append(text_node_to_html_node(node))
    return html_nodes






       


            