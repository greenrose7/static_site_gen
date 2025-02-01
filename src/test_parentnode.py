import unittest

from htmlnode import ParentNode, LeafNode

class TestParentNode(unittest.TestCase):
    def test_eq(self):
        childnode1 = LeafNode("p", "this is a test child node", {"color": "blue"})
        childnode2 = LeafNode("b", "this is a test child node too!", {"color": "red"})
        node1 = ParentNode("h1", [childnode1, childnode2], {"lang": "en", "test": "true"})
        node2 = ParentNode("h1", [childnode1, childnode2], {"lang": "en", "test": "true"})
        self.assertEqual(node1, node2)
    
    def test_to_html_multi_child(self):
        childnode1 = LeafNode("p", "this is a test child node", {"color": "blue"})
        childnode2 = LeafNode("b", "this is a test child node too!", {"color": "red"})
        node1 = ParentNode("h1", [childnode1, childnode2], {"lang": "en", "test": "true"})
        expected_output = "<h1 lang=\"en\" test=\"true\"><p color=\"blue\">this is a test child node</p><b color=\"red\">this is a test child node too!</b></h1>"
        self.assertEqual(node1.to_html(), expected_output)

    def test_to_html_nested_parents(self):
        childnode1 = LeafNode("h1", "this is a test child node")
        childnode2 = LeafNode("h2", "this is a test child node too!")
        childnode3 = LeafNode("h3", "this is a test child node three!")
        childnode4 = LeafNode("h4", "this is a test child node four!")
        node1 = ParentNode("d", [childnode1, childnode2])
        node2 = ParentNode("c", [childnode3, childnode4])
        node3 = ParentNode("b", [node1, node2])
        node4 = ParentNode("a", [node3])
        expected_output = "<a><b><d><h1>this is a test child node</h1><h2>this is a test child node too!</h2></d><c><h3>this is a test child node three!</h3><h4>this is a test child node four!</h4></c></b></a>"
        self.assertEqual(node4.to_html(), expected_output)

    def test_to_index_no_children(self):
        childnode1 = LeafNode("h1", "this is a test child node")
        node1 = ParentNode("a", [])
        with self.assertRaises(ValueError) as cm:
            node1.to_html()
        the_exception = cm.exception
        self.assertEqual(the_exception.args[0], "ParentNode must have children")

    def test_to_index_no_tags(self):
        childnode1 = LeafNode("h1", "this is a test child node")
        node1 = ParentNode(None, [childnode1])
        with self.assertRaises(ValueError) as cm:
            node1.to_html()
        the_exception = cm.exception
        self.assertEqual(the_exception.args[0], "ParentNode must have tag")



if __name__ == "__main__":
    unittest.main()