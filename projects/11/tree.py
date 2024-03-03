import xml.etree.ElementTree as ET


def tree(xml_string):
    class Node:
        def __init__(self, value, children=None):
            self.value = value
            self.children = children if children is not None else []

    def xml_to_tree(xml_string):
        root = ET.fromstring(xml_string)

        def build_tree(xml_element):
            # 假設每個節點要麼是一個值，要麼是一個表達式
            node_value = xml_element.text.strip() if xml_element.text else None
            # 對於有子節點 (子表達式) 的情況，遞迴建立子樹
            children = [build_tree(child) for child in xml_element]
            return Node(node_value, children)

        # 從 XML 的根元素開始建立樹
        return build_tree(root)

    # 將 XML 轉換成樹
    expr_tree = xml_to_tree(xml_string)

    # 輸出樹的結構來確認結果
    def print_tree(node, level=0):
        indent = "  " * level
        print(f"{indent}{node.value}")
        for child in node.children:
            print_tree(child, level + 1)

    print_tree(expr_tree)
