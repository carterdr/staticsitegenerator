import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)
        node = TextNode("This is a text node", "bold", "a")
        node2 = TextNode("This is a text node", "bold", "a")
        self.assertEqual(node, node2)
        node = TextNode("This is a text node", "baold")
        node2 = TextNode("This is a text node", "bold")
        self.assertNotEqual(node, node2)

    def test_url(self):
        node = TextNode("a", "b")
        self.assertEqual(None, node.url)
if __name__ == "__main__":
    unittest.main()