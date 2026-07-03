from enum import Enum

from htmlnode import ParentNode
from textnode import text_node_to_html_node, TextNode, TextType
from inline_markdown import text_to_textnodes


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    return [block.strip() for block in blocks if block.strip()]


def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith("#"):
        count = 0
        for c in block:
            if c == "#":
                count += 1
            else:
                break
        if 1 <= count <= 6 and len(block) > count and block[count] == " ":
            return BlockType.HEADING

    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    ordered = True
    for i, line in enumerate(lines):
        if not line.startswith(f"{i + 1}. "):
            ordered = False
            break
    if ordered:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.PARAGRAPH:
            text = block.replace("\n", " ")
            children.append(ParentNode("p", text_to_children(text)))

        elif block_type == BlockType.HEADING:
            level = 0
            for c in block:
                if c == "#":
                    level += 1
                else:
                    break
            text = block[level + 1 :]
            children.append(ParentNode(f"h{level}", text_to_children(text)))

        elif block_type == BlockType.CODE:
            text = block[3:-3].strip("\n")
            code_node = text_node_to_html_node(TextNode(text, TextType.CODE))
            children.append(ParentNode("pre", [code_node]))

        elif block_type == BlockType.QUOTE:
            lines = block.split("\n")
            text = "\n".join(line.lstrip(">").strip() for line in lines)
            children.append(ParentNode("blockquote", text_to_children(text)))

        elif block_type == BlockType.UNORDERED_LIST:
            lines = block.split("\n")
            items = []
            for line in lines:
                text = line[2:]
                items.append(ParentNode("li", text_to_children(text)))
            children.append(ParentNode("ul", items))

        elif block_type == BlockType.ORDERED_LIST:
            lines = block.split("\n")
            items = []
            for line in lines:
                text = line.split(". ", 1)[1]
                items.append(ParentNode("li", text_to_children(text)))
            children.append(ParentNode("ol", items))

    return ParentNode("div", children)
