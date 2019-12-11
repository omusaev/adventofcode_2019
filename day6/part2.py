from anytree import Node
from anytree.search import findall_by_attr

ORBIT_SYMBOL = ')'
COM = 'COM'
YOU = 'YOU'
SAN = 'SAN'
input_file = './input'


def _build_tree(parent, child_name, parent_child_relations):

    child = Node(child_name, parent=parent)

    for grandchild_name in parent_child_relations.get(child_name, []):
        _build_tree(child, grandchild_name, parent_child_relations)

    return child


def main():
    with open(input_file, 'r') as f:
        orbit_map = f.read().splitlines()

    print("Number of relations: {}".format(len(orbit_map)))
    parent_child_relations = {}

    for relation in orbit_map:
        object1_name, object2_name = relation.split(ORBIT_SYMBOL)

        object1_children = parent_child_relations.setdefault(object1_name, [])
        object1_children.append(object2_name)
    tree = _build_tree(None, COM, parent_child_relations)

    you_node = findall_by_attr(tree, YOU)[0]
    san_node = findall_by_attr(tree, SAN)[0]

    distance = None
    for i in range(you_node.depth):
        if you_node.ancestors[i] == san_node.ancestors[i]:
            continue

        distance = len(you_node.ancestors[i:]) + len(san_node.ancestors[i:])
        break

    print('Distance: {}'.format(distance))


if __name__ == '__main__':
    main()
