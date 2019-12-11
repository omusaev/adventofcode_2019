from anytree import Node

ORBIT_SYMBOL = ')'
COM = 'COM'
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

    root = _build_tree(None, COM, parent_child_relations)

    total_number = sum([node.depth for node in root.descendants])

    print('Total number of orbits: {}'.format(total_number))


if __name__ == '__main__':
    main()
