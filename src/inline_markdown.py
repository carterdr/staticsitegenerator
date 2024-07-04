from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link
)


import re

def extract_markdown_images(text):
    text_images = re.findall(r"!\[.*?\]\(.*?\)", text)
    output = []
    for text in text_images:
        split_text = text.split("]")
        alt_text = split_text[0][2:]
        image_link = split_text[1][1:-1]
        output.append((alt_text, image_link))
    return output
def extract_markdown_links(text):
    text_images = re.findall(r"\[.*?\]\(.*?\)", text)
    output = []
    for text in text_images:
        split_text = text.split("]")
        alt_text = split_text[0][1:]
        image_link = split_text[1][1:-1]
        output.append((alt_text, image_link))
    return output

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], text_type_text))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes
def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        original_text = node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(node)
            continue
        split_text = node.text
        for image_tup in images:
            combined = f"![{image_tup[0]}]({image_tup[1]})"
            split_text = split_text.split(combined, 1)
            if len(split_text) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if split_text[0] != "":
                new_nodes.append(TextNode(split_text[0],text_type_text))
            new_nodes.append(TextNode(image_tup[0], text_type_image, image_tup[1]))
            split_text = split_text[1]
        if split_text != "":
            new_nodes.append(TextNode(split_text,text_type_text))
    return new_nodes
def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        original_text = node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(node)
            continue
        split_text = node.text
        for link_tup in links:
            combined = f"[{link_tup[0]}]({link_tup[1]})"
            split_text = split_text.split(combined, 1)
            if len(split_text) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            if split_text[0] != "":
                new_nodes.append(TextNode(split_text[0],text_type_text))
            new_nodes.append(TextNode(link_tup[0], text_type_link, link_tup[1]))
            split_text = split_text[1]
        if split_text != "":
            new_nodes.append(TextNode(split_text,text_type_text))
    return new_nodes
def text_to_textnodes(text):
    nodes = [TextNode(text, text_type_text)]
    for delim, type in [("**", text_type_bold), ("*", text_type_italic), ("`", text_type_code)]:
        nodes = split_nodes_delimiter(nodes, delim, type)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
